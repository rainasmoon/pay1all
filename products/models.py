import datetime

from django.db import models
from django.template.defaultfilters import default
from django.utils import timezone;


# Create your models here.
class Product(models.Model):
    product_jd_skuid = models.BigIntegerField(default='0')
    product_name = models.CharField(max_length=200, default='no name')
    product_price = models.IntegerField(default=0)
    product_big_pic = models.CharField(max_length=200 , default='no pic')
    product_promotion_url = models.CharField(max_length=400, default='no url')
    p_scores = models.IntegerField(default=0)
    
    # the following a jd cid
    cid = models.IntegerField(default=0)
    cid2 = models.IntegerField(default=0)
    cid3 = models.IntegerField(default=0)
    cidName = models.CharField(max_length=100 , default='no name')
    cid2Name = models.CharField(max_length=100 , default='no name')
    cid3Name = models.CharField(max_length=100 , default='no name')
    
    wordcloud_pic_path = models.CharField(max_length=100, null=True)
    
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.product_name


class Search(models.Model):
    search_context = models.TextField()
    as_done = models.BooleanField(default=False)
    cid = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.search_context


class Menu(models.Model):
    menu_name = models.CharField(max_length=100, default='no menu')  # trim cidName to 100
    cid = models.IntegerField(default=0)
    m_scores = models.IntegerField(default=0)
    
    def __str__(self):
        return self.menu_name


class Order(models.Model):
    jd_order_id = models.BigIntegerField(default='0')
    jd_skuid = models.BigIntegerField(default='0')
    jd_sku_name = models.CharField(max_length=200, default='no name')
    jd_sku_num = models.IntegerField(default='0')
    jd_order_time = models.BigIntegerField(default='0')
    
    as_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.jd_order_id
    
