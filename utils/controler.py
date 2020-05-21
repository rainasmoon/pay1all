# -*- coding: utf-8 -*
from utils import crawler_jd
from utils import db_utils
from utils import db_utils_online_mysql as db_utils_online
from utils import export_jd_db


def do_job():
    if (db_utils.get_lock()):
        db_utils.lock()
        print("GET LOCKED.")
        search_list = db_utils_online.select_search()
        print("JOBS NO.:" + str(len(search_list)))
        for asearch in search_list:
            # first colmon is id , second is context
            search_id = asearch[0]
            search_context = asearch[1]
            print('SEARCH JD FOR:' + search_context)
            if search_context.isdigit():
                r_sku_list = [search_context]
            else:
                r_sku_list = crawler_jd.call_jd_search(search_context)
            for i in r_sku_list:
                # the 1 item is sku
                db_utils.insert_db(i)
            print("STORE THEM:" + str(len(r_sku_list)))
            export_jd_db.make_jd_data()
            db_utils_online.done_search(search_id)
            print("SEARCH ONE DONE.")
        print("START MAKE CLOUD PIC ...")
        export_jd_db.make_jd_wordcloud_comment()
        print("END MAKE CLOUD PIC.")
        print('START MY ORDER...')
        export_jd_db.make_jd_myorder()
        print('END MY ORDER.')
        print('SYNC JD ORDER...')
        export_jd_db.query_jd_myorder()
        print('SYNC JD ORDER END.')
        print('UPDATE PROMOTION URL...')
        export_jd_db.make_jd_promotion_url()
        print('UPDATE PROMOTIONURL END.')
        db_utils.unlock()
        print("UNLOCKED. SUCCESS>>>>>>>>>>>>>>>>>>>")
    else:
        print('CANT LOCKED...PLS CHECK.')


def init():
    db_utils.init_db()


def init_job():
    print('INIT...')
    export_jd_db.init_jd_myorder()
    print('END.')


def reset():
    db_utils.reset()
    db_utils_online.reset()


def unlock():
    db_utils.unlock()


if __name__ == '__main__':
    do_job()

