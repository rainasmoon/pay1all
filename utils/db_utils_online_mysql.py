# -*- coding: utf-8 -*
import pymysql

'''
'''


def get_mysql_conn():
    return  pymysql.connect(host='localhost', port=3306, user='pc', passwd='pc', db='online_db', charset='utf8', use_unicode=True)


def get_conn():
    return get_mysql_conn()


def insert_product(param):
    conn = get_conn()
    c = conn.cursor()
    c.execute('select 1 from products_product where product_jd_skuid = %s', (param['product_jd_skuid'],))
    if not c.fetchall():
        c.execute('''INSERT INTO products_product(product_jd_skuid, product_name, product_price, product_big_pic, product_promotion_url, p_scores, cid, cid2, cid3, cidName, cid2Name, cid3Name, pub_date) 
        VALUES (%(product_jd_skuid)s, %(product_name)s, %(product_price)s, %(product_big_pic)s, %(product_promotion_url)s, %(p_scores)s, %(cid)s, %(cid2)s, %(cid3)s, %(cidName)s, %(cid2Name)s, %(cid3Name)s, %(pub_date)s)''', param)
        print('ONLINE DB, INSERT SKU:', param['product_jd_skuid'])
    else:
        print('ONLINE DB, SKU EXISTS:', param['product_jd_skuid'])
    conn.commit()
    conn.close()


def insert_menu(param):
    conn = get_conn()
    c = conn.cursor()
    c.execute('select 1 from products_menu where menu_name = %s', (param['menu_name'],))
    if not c.fetchall():
        c.execute('''INSERT INTO products_menu(menu_name, cid, m_scores) 
                VALUES( %(menu_name)s, %(cid)s, %(m_scores)s)''', param)
        print('ONLINE DB, INSERT MENU :', param['menu_name'])
    else:
        pass
        
    conn.commit()
    conn.close()


def insert_order(param):
    conn = get_conn()
    c = conn.cursor()
    c.execute('select 1 from products_order where jd_order_id = %s and jd_skuid = %s', (param['jd_order_id'], param['jd_skuid']))
    if not c.fetchall():
        c.execute('''INSERT INTO products_order( jd_order_id, jd_skuid, jd_sku_name, jd_sku_num, jd_order_time, as_done) 
        VALUES (%(jd_order_id)s, %(jd_skuid)s, %(jd_sku_name)s, %(jd_sku_num)s, %(jd_order_time)s, %(as_done)s)''', param)
        print('ONLINE DB, INSERT ORDER:', param['jd_order_id'], param['jd_skuid'])
    else:
        print('ONLINE DB, ORDER EXISTS:', param['jd_order_id'], param['jd_skuid'])
    conn.commit()
    conn.close()


def select_product(sku_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, p_scores from products_product where product_jd_skuid = %s', (sku_id,))
    r = c.fetchone()
    conn.commit()
    conn.close()
    return r 


def select_search():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, search_context from products_search where as_done = 0')
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r 


def select_no_promotion_url_product():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, product_jd_skuid from products_product where product_promotion_url = \'\'')
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r 

def select_no_wordcloud_product():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, product_jd_skuid from products_product where wordcloud_pic_path is null')
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r 


def select_order():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, jd_skuid from products_order where as_done = 0')
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r 


def get_recent_order_time():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select max(jd_order_time) from products_order')
    r = c.fetchone()
    conn.commit()
    conn.close()
    return r[0] 


def done_search(iid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set as_done = 1 WHERE id = %s', (iid,))
    conn.commit()
    conn.close() 


def done_order(iid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_order set as_done = 1 WHERE id = %s', (iid,))
    conn.commit()
    conn.close() 


def reset():
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set as_done = 0')
    conn.commit()
    conn.close() 


def update_product_scores(iid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_product set p_scores = p_scores+1 WHERE id = %s', (iid))
    conn.commit()
    conn.close() 


def update_search_cid(iid, cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set cid = %s WHERE id = %s', (cid, iid))
    conn.commit()
    conn.close() 


def update_promotion_url(iid, promotion_url):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_product set product_promotion_url  = %s WHERE id = %s', (promotion_url, iid))
    conn.commit()
    conn.close()

def update_wordcloud_pic_path(iid, wordcloud_pic_path):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_product set wordcloud_pic_path = %s WHERE id = %s', (wordcloud_pic_path, iid))
    conn.commit()
    conn.close()

    
def select_products():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select * from  products_product')
    print('PRODUCTS TABLE ITEMS:', c.fetchall())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    select_product(0)
