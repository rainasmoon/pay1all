from django.test import TestCase
from django.utils import timezone

from products.models import Product

# Create your tests here.


class ProductModelTests(TestCase):

    def setUp(self):
        Product.objects.create(product_jd_skuid='1001', product_name='aproduct', product_price=100, product_big_pic='http://a.com/bigpic.jpg', product_promotion_url='http://j.com/click?XXXX', p_scores=1500, pub_date=timezone.now())
        Product.objects.create(product_jd_skuid='1002', product_name='anotherproduct', product_price=100, product_big_pic='http://a.com/bigpic.jpg', product_promotion_url='http://j.com/click?XXXX', p_scores=1500, pub_date=timezone.now())
        
    def test_has_promotion_url(self):
        aproduct = Product.objects.get(product_jd_skuid='1001')
        self.assertTrue(aproduct.product_promotion_url)
