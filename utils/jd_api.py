# -*- coding: UTF-8 -*- 
'''
Created on 2019-10-23

@author: Administrator
'''

import datetime
import hashlib
from io import StringIO
import json
import time
from urllib import parse
from urllib import request

f = open('config_api.json', 'r')
config_jd_api = json.load(f)
app_key = config_jd_api['jd_app_key']
appsecret = config_jd_api['jd_appsecret']
site_id = '1728182420'
position_id = '1915772300'
access_token = ''

method_get_promotion = 'jd.union.open.promotion.common.get'
method_get_category = 'jd.union.open.category.goods.get'
method_get_goods = 'jd.union.open.goods.promotiongoodsinfo.query'
method_order = 'jd.union.open.order.query'
method_jingfen = 'jd.union.open.goods.jingfen.query'

test_jd_prod_sku_1 = 25643981948

STATUS_OK = 200


def get_material_id(jd_prod_sku):
    return 'https://item.jd.com/' + str(jd_prod_sku) + '.html'


def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_param_json_promotion_url(material_id):
    return '{"promotionCodeReq":{"siteId":"' + site_id + '","materialId":"' + material_id + '","positionId":"' + position_id + '"}}'


def get_param_json_goods_100(goods_sku_array):
    # the max is 100 i.e: 1000,1002,1113,
    return '{"skuIds":"' + goods_sku_array + '"}'


def get_param_json_category(paraent_id, agrade):
    return '{"req":{"parentId":' + str(paraent_id) + ',"grade":' + str(agrade) + '}}'


def get_param_json_orders(atime, page_no):
    return '{"orderReq":{"time":"' + atime + '","pageNo":' + str(page_no) + ',"pageSize":"500","type":"1"}}'


def get_param_json_jingfen():
    '''
    频道id：1-好券商品,2-超级大卖场,10-9.9专区,22-热销爆品,24-数码家电,25-超市,26-母婴玩具,27-家具日用,28-美妆穿搭,29-医药保健,30-图书文具,31-今日必推,32-王牌好货
    排序字段(price：单价, commissionShare：佣金比例, commission：佣金， inOrderCount30DaysSku：sku维度30天引单量，comments：评论数，goodComments：好评数)
    '''
    return '{"goodsReq":{"eliteId":1,"pageIndex":1,"pageSize":50,"sortName":"inOrderCount30DaysSku","sort":"asc"}}'


def get_sign_key(method, timestamp, param_json):
    
    c = ''
    # c = c + 'access_token' + access_token
    c = c + 'app_key' + app_key
    c = c + 'formatjson'
    c = c + 'method' + method
    c = c + 'param_json' + param_json
    c = c + 'sign_methodmd5'
    c = c + 'timestamp' + timestamp
    c = c + 'v1.0'
    c = appsecret + c + appsecret
    sign_key = hashlib.md5(c.encode("utf-8")).hexdigest().upper()
    return sign_key
    

def get_api_url(method, param_json):
    timestamp = get_timestamp()
    
    sign_key = get_sign_key(method, timestamp, param_json)
    return 'https://router.jd.com/api?v=1.0&method=' + method + '&access_token=&app_key=' + app_key + '&sign_method=md5&format=json&timestamp=' + parse.quote(timestamp) + '&sign=' + sign_key + '&param_json=' + param_json


def call_jd_api(api_url):
    # print('CALL JD API:' + api_url)
    rresponse = request.urlopen(api_url)
    s_result = rresponse.read()
    # print('JD RESPONSES:' + str(s_result))
    json_result = json.loads(s_result)  
    return json_result

    
def call_jd_promotion_url(sku):
    material_id = get_material_id(sku)
    param_json = get_param_json_promotion_url(material_id)
    json_result = call_jd_api(get_api_url(method_get_promotion, param_json))
    r_result = json_result['jd_union_open_promotion_common_get_response']['result']
    inner_json_result = json.load(StringIO(r_result))
    if inner_json_result['code'] == STATUS_OK:
        click_url = inner_json_result['data']['clickURL']
        return click_url
    else:
        print('JD ERROR:' + r_result)

    
def call_jd_goods_detail(sku_list):
    param_json = get_param_json_goods_100(sku_list)
    json_result = call_jd_api(get_api_url(method_get_goods, param_json))
    r_result = json_result['jd_union_open_goods_promotiongoodsinfo_query_response']['result']
    inner_json_result = json.load(StringIO(r_result))
    
    goods_json = inner_json_result['data']

    return goods_json

    
def call_jd_category(paraent_id, agrade):
    '''
    paraent_id : 0 will show 一级目录
    agrade: 0, 1, 2
    '''
    param_json = get_param_json_category(paraent_id, agrade)
    json_result = call_jd_api(get_api_url(method_get_category, param_json))
    return json_result


def call_my_orders(atime, page_no):
    r = []
    param_json = get_param_json_orders(atime, page_no)
    json_result = call_jd_api(get_api_url(method_order, param_json))
    r_result = json_result['jd_union_open_order_query_response']['result']
    inner_json_result = json.load(StringIO(r_result))
    if inner_json_result['hasMore'] != False:
        print("$$$$$$$$$$$$$$$$WARNING$$$$$$$$$$$$$$$$HASMORE:", inner_json_result['hasMore'])
    
    if 'data' in inner_json_result:
        r_order_list = inner_json_result['data']
        print('INFO: FIND orders : ', len(r_order_list))
        for aorder in r_order_list:
            orderId = aorder['orderId']
            orderTime = aorder['orderTime']
            if aorder['parentId'] != 0:
                print('SUB ORDER:', aorder['parentId'])
                continue
            asku_list = aorder['skuList']
            print('INFO: FIND:SKU', len(asku_list))
            for asku in asku_list:
                skuId = asku['skuId']
                skuName = asku['skuName']
                skuNum = asku['skuNum']
                r.append({'orderId':orderId, 'orderTime':orderTime, 'skuId':skuId, 'skuName':skuName, 'skuNum':skuNum})
                
        return r


def call_jingfen():
    param_json = get_param_json_jingfen()
    json_result = call_jd_api(get_api_url(method_jingfen, param_json))
    return json_result  


if __name__ == '__main__':
#     r = call_jd_promotion_url(test_jd_prod_sku_1)
#     print(r)
#     r = call_jd_category(0, 0)
#     print(r)
   
     r = call_jingfen()
     print(r)
