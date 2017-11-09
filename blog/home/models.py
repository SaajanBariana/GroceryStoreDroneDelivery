# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Accounts(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)

class Cart(models.Model):
    username = models.CharField(max_length = 100)
    itemNum = models.IntegerField()
    qty = models.IntegerField()
    weight = models.IntegerField()
    price = models.IntegerField()
    itemName = models.CharField(max_length = 100)
    itemImg = models.CharField(max_length = 100)

# Create your models here.
