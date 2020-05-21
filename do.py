# -*- coding: UTF-8 -*- 
import time

from utils import controler as c

print ('START:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
c.do_job()
print ('END:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
