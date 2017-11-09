# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey( Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text

class Items(models.Model):
    item_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    weight = models.IntegerField()
    cost = models.DecimalField(max_digits = 5, decimal_places = 2)
    quantity = models.IntegerField()
    tags = models.CharField(max_length = 100),
    description = models.CharField(max_length = 100)

    def __str__(self):
        return self.question_text

# Create your models here.
