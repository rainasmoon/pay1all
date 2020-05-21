# prepare env

pip install mysqlclient  # i use this.
python3 -m pip install --upgrade pip
yum install wqy-zenhei-fonts
python3 -m pip install --upgrade pip
python3 -m pip install pymysql
python3 -m pip install jieba
python3 -m pip install wordcloud
python3 -m pip install requests
python3 -m pip install matplotlib

# init the data

python manage.py loaddata test/fixtures/init_product
python manage.py createsuperuser

usermod -a -G hht uwsgi
need to MAKE SURE you use THE REAL API

# start script

uwsgi --chdir=/home/hht/pay1all --http :8000 --module pay1all.wsgi:application  --master --pidfile=/tmp/pay1all-master.pid  --processes=5 --vacuum --daemonize=/home/hht/pay1all.log 

uwsgi --chdir=/home/pi/git/online-application/pay1all --http :8000 --module pay1all.wsgi:application  --master --pidfile=/tmp/pay1all-master.pid  --vacuum --daemonize=/home/pi/pay1all.log 
 
# tips

https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=58d2347f9b31410588c47ce29351c7be

curl https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=c060319d4120468ca810e38ab6b73545 -x http://121.199.36.121:3128 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"

curl  https://so.m.jd.com/ware/search.action?keyword=%E6%89%8B%E6%9C%BA&searchFrom=home&sf=11&as=1  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"



