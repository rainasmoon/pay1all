# -*- coding: utf-8 -*
import sqlite3
ONLINE_DB = 'db.sqlite3'

'''
deprected.
'''


def get_sqlite_conn():
    return sqlite3.connect(ONLINE_DB)


def get_conn():
    return get_sqlite_conn()


def insert_db(param):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO products_product(product_jd_skuid, product_name, product_price, product_big_pic, product_promotion_url, p_scores, cid, cid2, cid3, cidName, cid2Name, cid3Name, pub_date) 
                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? 
                WHERE NOT EXISTS(SELECT 1 FROM products_product WHERE product_jd_skuid = ?)''', (param['product_jd_skuid'], param['product_name'], param['product_price'], param['product_big_pic'], param['product_promotion_url'], param['p_scores'], param['cid'], param['cid2'], param['cid3'], param['cidName'], param['cid2Name'], param['cid3Name'], param['pub_date'], param['product_jd_skuid']))
    conn.commit()
    conn.close()


def insert_menu(param):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO products_menu(menu_name, cid, m_scores) 
                SELECT ?, ?, ?
                WHERE NOT EXISTS(SELECT 1 FROM products_menu WHERE cid = ?)''', (param['menu_name'], param['cid'], param['m_scores'], param['cid']))
    conn.commit()
    conn.close()


def select_search():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select id, search_context from products_search where as_done = 0')
    r = c.fetchall()
    conn.commit()
    conn.close()
    return r 


def search_done(iid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set as_done = 1 WHERE id = ?', (iid,))
    conn.commit()
    conn.close() 


def reset():
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set as_done = 0')
    conn.commit()
    conn.close() 


def search_update(iid, cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute('update products_search set cid = ? WHERE id = ?', (cid, iid))
    conn.commit()
    conn.close() 

    
def select_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('select * from  "products_product" ')
    print('PRODUCTS TABLE ITEMS:' + c.fetchall())
    conn.commit()
    conn.close()

