# -*- coding: utf-8 -*
'''
response.cookies
response.headers
response.status_code
response.url

DAY2: the call frequency ratio limitation

'''

import json
import random
import re
from urllib import parse
from urllib import request
import urllib
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

test_asearch_input_1 = '手机'

MAX_TRY = 5


def create_search_url(keyword):
    keyword = parse.quote(keyword)
    return 'https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&wq=' + keyword + '&pvid=c060319d4120468ca810e38ab6b73545'


def create_search_url_mobile(keyword):
    keyword = parse.quote(keyword)
    return 'https://so.m.jd.com/ware/search.action?keyword=' + keyword + '&searchFrom=home&sf=11&as=1'


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
]

aheaders = {
    'Host': 'search.jd.com',
    'User-Agent': random.choice(USER_AGENTS),
    'Referer': 'https://www.jd.com/',
    'Cookie': '',
    }


def call_jd_search(keyword):
    aurl = create_search_url(keyword)
    print('CRAWEL JD FOR:' + aurl)
    rresponse = use_no_proxy(aurl)
    rlist = re.findall(r'(//item.jd.com/)([0-9]*)(.html)', rresponse)
    print("YEAH: FIND ITEMS NO.:" + str(len(rlist)))
    if len(rlist) == 0:
        rresponse = use_proxy(aurl)
        count = 0
        while rresponse == None and count < MAX_TRY:
            print('PROXY ERROR, CALL AGAIN')
            count += 1
            rresponse = use_proxy(aurl)   
        rlist = re.findall(r'(//item.jd.com/)([0-9]*)(.html)', rresponse)
        print("YEAH: FIND ITEMS VIA PROXY NO.:" + str(len(rlist)))
    
    r_sku_list = [i[1] for i in rlist]    
    return r_sku_list


def use_proxy(aurl):
    proxy = call_a_new_proxy()
    print('USE PROXY:' + proxy)
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    })
    
    opener = build_opener(proxy_handler)
    try:
        f = opener.open(aurl)
        r = f.read().decode('utf-8')
        return r
    except URLError as err:
        print('ERROR PROXY', err)


def call_a_new_proxy():
    a_proxy_url = 'http://118.24.52.95/get/'
    with request.urlopen(a_proxy_url) as response:
        r_json = json.load(response)
        new_proxy = r_json['proxy']
        
    return new_proxy


def use_no_proxy(aurl):
    req = request.Request(url=aurl, headers=aheaders)
    try:
        response = request.urlopen(req)
        rresponse = response.read().decode('utf-8', "ignore") 
        return rresponse
    except URLError as err:
        print ("ERROR WHEN CONNECTING:", err)


if __name__ == '__main__':
    r = call_jd_search(test_asearch_input_1)
    print(r)
