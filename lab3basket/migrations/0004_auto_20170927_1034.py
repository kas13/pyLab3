# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab3basket', '0003_auto_20170827_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketmodel',
            name='path',
            field=models.CharField(default='', max_length=123, verbose_name='basket path'),
        ),
        migrations.AlterField(
            model_name='basketmodel',
            name='basket_name',
            field=models.CharField(max_length=123, verbose_name='basket name'),
        ),
    ]
