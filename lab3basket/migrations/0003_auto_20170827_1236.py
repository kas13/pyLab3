# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab3basket', '0002_auto_20170827_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basketmodel',
            name='files',
        ),
        migrations.AlterField(
            model_name='basketmodel',
            name='basket_name',
            field=models.CharField(max_length=123),
        ),
    ]
