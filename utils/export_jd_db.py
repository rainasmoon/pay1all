# -*- coding: utf-8 -*
import datetime
from io import StringIO
import json
import time

from utils import db_utils_online_mysql as db_utils_online, \
    db_utils_online_mysql
from utils import jd_api, db_utils
from utils import jd_comment

MAX_PARAM = 100 


def make_menu_param(agood):
    field_json = {}
    field_json['menu_name'] = agood['cid3Name']
    field_json['cid'] = agood['cid3']
    field_json['m_scores'] = 1500
    return field_json


def make_produst_param(agood):
    field_json = {}
    sku = agood['skuId']
    field_json['product_jd_skuid'] = sku
    field_json['product_name'] = agood['goodsName']
    field_json['product_price'] = agood['unitPrice']
    field_json['product_big_pic'] = agood['imgUrl']
    url = jd_api.call_jd_promotion_url(sku)
    if not url:
        print('WARN:::NOT URL for ', sku)
        url = '/'        
    field_json['product_promotion_url'] = url
    field_json['p_scores'] = 1500
    
    field_json['cid'] = agood['cid']
    field_json['cid2'] = agood['cid2']
    field_json['cid3'] = agood['cid3']
    field_json['cidName'] = agood['cidName']
    field_json['cid2Name'] = agood['cid2Name']
    field_json['cid3Name'] = agood['cid3Name']
    
    field_json['pub_date'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    return field_json


def make_order_param(aorder, as_done=False):
    field_json = {}
    field_json['jd_order_id'] = aorder['orderId']
    field_json['jd_skuid'] = aorder['skuId']
    field_json['jd_sku_name'] = aorder['skuName']
    field_json['jd_sku_num'] = aorder['skuNum']
    field_json['jd_order_time'] = aorder['orderTime']
    
    field_json['as_done'] = as_done
    
    return field_json

def not_skip_good(agood):
    # 737 | 16962 | 16965 |
    if agood['cid3']==16965:
        # 家电维修 商品
        return False
    return True

def make_jd_data():
    r_set = db_utils.select_sku()
    print('FIND NEW SKU NO.:', len(r_set))
    jd_sku_list = r_set
    for j in range(len(jd_sku_list))[::MAX_PARAM]:
        t_sku_100_list = (','.join(jd_sku_list[j:j + MAX_PARAM]))
        goods_list = jd_api.call_jd_goods_detail(t_sku_100_list)
        for agood in goods_list:    
            if not_skip_good(agood):
                db_utils_online.insert_product(make_produst_param(agood))
                db_utils_online.insert_menu(make_menu_param(agood))
            else:
                print('SKIP A GOOD: ', agood)
            db_utils.done(agood['skuId'])
    print('INSERT PRODUCT, MENU, SET STORE TO DONE SUCCESS.')

    
def make_jd_promotion_url():
    r_set = db_utils_online_mysql.select_no_promotion_url_product()
    print('FIND NO promotion url NO....:', len(r_set))
    for item in r_set:
        item_id = item[0]
        sku_id = item[1]
        promotion_url = jd_api.call_jd_promotion_url(sku_id)
        if promotion_url:
            db_utils_online_mysql.update_promotion_url(item_id,
                                                            promotion_url)
            print('UPDATE promotion url SUCCESS:', item_id)
        else:
            print('SKIP. promotion_url EMPTY,:', promotion_url)

def make_jd_wordcloud_comment():
    r_set = db_utils_online_mysql.select_no_wordcloud_product()
    print('FIND NO CLOUDPIC NO....:', len(r_set))
    for item in r_set:
        item_id = item[0]
        sku_id = item[1]
        jd_comment.batch_spider_comment(sku_id)
        wordcloud_pic_path = jd_comment.create_word_cloud(sku_id)
        if wordcloud_pic_path:
            db_utils_online_mysql.update_wordcloud_pic_path(item_id, wordcloud_pic_path)
            print('UPDATE PIC PATH SUCCESS:', item_id)
        else:
            print('SKIP. WORDCLOUD PIC PATH EMPTY,:', wordcloud_pic_path)


def init_jd_myorder():    
    # inner_init_jd_myorder(datetime.date(2019, 10, 1), datetime.date(2019, 11, 13))
    pass


def query_jd_myorder():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    recent = db_utils_online_mysql.get_recent_order_time()
    if recent:
        begin = datetime.date.fromtimestamp(recent / 1000)
        print('QUERY JD MYORDER', begin, yesterday)
        inner_init_jd_myorder(begin, yesterday)

    
def inner_init_jd_myorder(begin, end):
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        aday = day.strftime("%Y%m%d")
        for i in range(24):
            atime = aday + str(i).zfill(2)
            print("CALL MYORDER FOR:", atime)
            order_list = jd_api.call_my_orders(atime, 1)
            if not order_list:
                print('NONE.')
                continue
            for order in order_list:
                askuid = order['skuId']
                aproduct = db_utils_online_mysql.select_product(askuid)
                if aproduct:
                    iid = aproduct[0]
                    p_scores = aproduct[1]
                    print("ADD PRODUCT SCORE:", p_scores)
                    db_utils_online_mysql.update_product_scores(iid)
                    aparam = make_order_param(order, as_done=True)
                else:
                    print("ADD SKUID TO STORE:", askuid)
                    db_utils.insert_db(askuid)
                    aparam = make_order_param(order, as_done=False)
                db_utils_online_mysql.insert_order(aparam)


def make_jd_myorder():
    r_set = db_utils_online_mysql.select_order()
    print('FIND NEW ORDERS NO.>>>:', len(r_set))
    for aorder in r_set:
        iid = aorder[0]
        askuid = aorder[1]
        aproduct = db_utils_online_mysql.select_product(askuid)
        if aproduct:
            product_id = aproduct[0]
            p_scores = aproduct[1]
            print('UPDATE PRODUCT SCORES, {}, {}', product_id, p_scores)
            db_utils_online_mysql.update_product_scores(product_id)
            db_utils_online.done_order(iid)
        else:
            print('ADD SKUID TO STORE:', askuid)
            db_utils.insert_db(askuid)
        
