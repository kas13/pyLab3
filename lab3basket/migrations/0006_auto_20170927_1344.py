# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab3basket', '0005_auto_20170927_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketmodel',
            name='path',
            field=models.CharField(default='/home/student/basket', max_length=123, verbose_name='basket path'),
        ),
    ]
