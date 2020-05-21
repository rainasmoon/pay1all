# -*- coding: utf-8 -*

import json
import os
import random
import time

import jieba
import requests

import numpy as np
from wordcloud import WordCloud, STOPWORDS

STATIC_PIC_PATH = '/var/www/html/static/cloudpic/'
COMMENT_FILE_PATH = STATIC_PIC_PATH + 'jd_comment.txt'
# 词云字体
WC_FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'

MAX_PAGE_NUM = 10

test_jd_prod_sku_1 = 25643981948


def spider_comment(sku_id, page=0):
    """
    爬取京东指定页的评价数据
    :param page: 爬取第几，默认值为0
    """
    url = f'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4646&productId={sku_id}' \
          f'&score=0&sortType=5&page={page}&pageSize=10&isShadowSku=0&fold=1'
    kv = {'user-agent': 'Mozilla/5.0', 'Referer': f'https://item.jd.com/{sku_id}.html'}

    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
    except:
        print('ERROR: 爬取失败:', url)
        return False
    # 截取json数据字符串
    r_json_str = r.text[26:-2]
    r_json_obj = json.loads(r_json_str)
    # 获取评价列表数据
    if 'comments' not in r_json_obj:        
        print("NO JDCOMMENTS IN HTML, PLS CHECK...")
        return False
    r_json_comments = r_json_obj['comments']
    if len(r_json_comments) == 0 :
        print("NO JDCOMMENTS, PLS CHECK...")
        return False
    for r_json_comment in r_json_comments:
        # 以追加模式换行写入每条评价
        with open(COMMENT_FILE_PATH + str(sku_id), 'a+') as file:
            file.write(r_json_comment['content'] + '\n')
            
    return True


def batch_spider_comment(sku_id):
    """
    批量爬取某东评价
    """
    if not os.path.exists(COMMENT_FILE_PATH + str(sku_id)):  
        print('SPIDER JD COMMENT...:', sku_id, ':', MAX_PAGE_NUM)        
        for i in range(MAX_PAGE_NUM):
            r = spider_comment(sku_id, i)
            if not r :
                break
            time.sleep(random.random() * 5)


def cut_word(sku_id):
    """
    对数据分词
    :return: 分词后的数据
    """
    if os.access(COMMENT_FILE_PATH + str(sku_id), os.R_OK):
        try:
            with open(COMMENT_FILE_PATH + str(sku_id)) as file:
                comment_txt = file.read()
                wordlist = jieba.cut(comment_txt, cut_all=True)
                wl = " ".join(wordlist)
                return wl
        except:
            print('ERROR COMMENT FILE:', sku_id)

    else:
        print('JD COMMENT FILE NOT EXIST:', sku_id)


def create_word_cloud(sku_id):
    """
    生成词云
    :return:
    """
    cloud_pic_file_name = f'result{sku_id}.png'
    r_file_path = STATIC_PIC_PATH + cloud_pic_file_name
    stopwords = set()
    f_stopword = open('stopwords.txt', 'r')
    for line in f_stopword.readlines():
        stopwords.add(line.strip())
 
    if not os.path.exists(r_file_path):
        print('MAKE CLOUD PIC...:', r_file_path)
        # 设置词云的一些配置，如：字体，背景色，词云形状，大小
        wc = WordCloud(background_color="white", max_words=2000, stopwords=stopwords, scale=4,
                       max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
        # 生成词云
        r_cutword = cut_word(sku_id)
        if r_cutword:
            wc.generate(r_cutword)
    
            wc.to_file(r_file_path)
            print('MAKE SUCCESS:', r_file_path)
            return cloud_pic_file_name
        else:
            print('NO CUTWORD, NO PIC CREATED, NO PATH')
    else:
        print('CLOUD PIC EXIST:', r_file_path)
        return cloud_pic_file_name


if __name__ == '__main__':
    # 爬取数据
    batch_spider_comment(test_jd_prod_sku_1)

    # 生成词云
    r_file_path = create_word_cloud(test_jd_prod_sku_1)
    print(r_file_path)
