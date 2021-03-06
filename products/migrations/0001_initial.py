# Generated by Django 2.2.6 on 2019-11-01 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(default='no menu', max_length=100)),
                ('cid', models.IntegerField(default=0)),
                ('m_scores', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_jd_skuid', models.BigIntegerField(default='0')),
                ('product_name', models.CharField(default='no name', max_length=200)),
                ('product_price', models.IntegerField(default=0)),
                ('product_big_pic', models.CharField(default='no pic', max_length=200)),
                ('product_promotion_url', models.CharField(default='no url', max_length=400)),
                ('p_scores', models.IntegerField(default=0)),
                ('cid', models.IntegerField(default=0)),
                ('cid2', models.IntegerField(default=0)),
                ('cid3', models.IntegerField(default=0)),
                ('cidName', models.CharField(default='no name', max_length=100)),
                ('cid2Name', models.CharField(default='no name', max_length=100)),
                ('cid3Name', models.CharField(default='no name', max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_context', models.TextField()),
                ('as_done', models.BooleanField(default=False)),
                ('cid', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
