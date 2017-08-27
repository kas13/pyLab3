# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import jsonfield


# Create your models here.


class BasketModel(models.Model):
    basket_name = models.CharField(max_length=123)
    #files = models.TextField()

    class Meta:
        db_table = "Basket"

    def __str__(self):
        return self.basket_name
