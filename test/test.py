import datetime
from io import StringIO
import json
import re
import time
from urllib import parse
from urllib import request
import urllib
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

from utils import db_utils
from utils.elo import Elorating


def test_json():
    print("json:")
    s = b'{"main":{"result":{"code":200, "data":[{"name":"name1"},{"name":"name2"}]}}}'
    j = json.loads(s)
    print(j)
    print(j['main'])    
    print(j['main']['result']['data'][0])
    print(j['main']['result']['data'][0]['name'])


def test_str():
    print('{0}, {1}, {2}'.format(5, 10.0, 100))
    print('{0},{1}'.format(1 / 2, 1 / 3))


def test_slice_array():
    r = []
    for i in range(100):
        r.append(str(i))
    print(r[::10])  
    MAX_PARAM = 10  
    for j in range(len(r))[::MAX_PARAM]:
        print(','.join(r[j:j + MAX_PARAM]))


def test_set():
    l1 = [1, 2, 3, 1, 2]
    l2 = [2, 3, 4]
    r = set()
    r = r | set(l1)
    r = r | set(l2)
    print(r)


def test_StringIO():
    print(StringIO('you are right.'))
    print(json.loads(r'[1,2,3,4]'))


def test_import_set():
    r_set = set()
    
    fi = open('crawler_jd.list', 'r')
    for line in fi:
        print(line)
        print(json.loads(line))
    fi.close()


def test_parse_quote():
    print(parse.quote('a b'))
    print(parse.quote('a今天b'))


def test_index():
    seq = [i for i in range(10, 20)]
    print(seq)
    print(seq[3])
    print(seq.index(seq[3]))
    
    for a, i in enumerate(seq):
        print(a, i)


def test_lock():    
    print(db_utils.get_lock())
#     db_utils.lock()
    print(db_utils.get_lock())
    db_utils.unlock()
    print(db_utils.get_lock())


def call_a_new_proxy():
    a_proxy_url = 'http://118.24.52.95/get/'
    with request.urlopen(a_proxy_url) as response:
        r_json = json.load(response)
        return r_json['proxy']


def test_proxy():
    proxy = call_a_new_proxy()
    print('use proxy:' + proxy)
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
    })
    opener = build_opener(proxy_handler)
    try:
        response = opener.open('https://www.rainasmoon.com/me.html')
        print(response.read().decode('utf-8'))
    except URLError as e:
        print(e.reason)


def test_proxy_1():
    aurl = 'http://ifconfig.co/'
    aurl = 'https://www.rainasmoon.com/me.html'
    proxy = call_a_new_proxy()
    print('USE PROXY:' + proxy)
    proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    req = request.Request(url=aurl)
    response = request.urlopen(req)   
    rresponse = response.read().decode('utf-8', "ignore") 
    print(rresponse)


def test_proxy_2():
    aurl = 'https://www.rainasmoon.com/me.html'
    proxy = call_a_new_proxy()
    print('use proxy:' + proxy)
    proxy_handler = ProxyHandler({
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    })
    
    opener = build_opener(proxy_handler)
    try:
        f = opener.open(aurl)
        r = f.read().decode('utf-8')
        
        print(r)
    except URLError as err:
        print('ERROR PROXY', err)


def test_date():
    begin = datetime.date(2019, 11, 1)
    end = datetime.date(2019, 11, 13)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        print(day.strftime("%Y%m%d"))
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    print(yesterday)
    now = int(round(time.time() * 1000))
    print(now)
    begin = datetime.date.fromtimestamp(now / 1000)
    print(begin)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        aday = day.strftime("%Y%m%d")
        for i in range(24):
            atime = aday + str(i).zfill(2)
            print("CALL MYORDER FOR:", atime)
            
    print('QUERY JD MYORDER', begin, yesterday)

        
def test_str_2():
    for i in range(24):
        print(str(i).zfill(2))


def test_re():
    print('1111'.isdigit())
    print('a1111'.isdigit())


# test_re()
test_date()
# test_str_2()
# test_proxy_2()    
# test_index()
# test_parse_quote()
# test_StringIO()
# test_import_set()
# test_set()
# test_str()
# test_slice_array()
