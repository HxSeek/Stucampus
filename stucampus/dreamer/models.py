#-*- coding: utf-8 -*-
from django.db import models
from stucampus.custom.model_field import MultiSelectField


class Application(models.Model):

    SEX = (
        (u'男', u'男'),
        (u'女', u'女'),
    )

    DEPARTMENT = (
        (u'技术部', u'技术部'),
        (u'办公室', u'办公室'),
        (u'美工部', u'美工部'),
        (u'采编部', u'采编部'),
    )

    stu_num = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    college = models.CharField(max_length=30)
    sex = models.CharField(max_length=5, choices=SEX)
    volunteers = MultiSelectField(max_length=15, choices=DEPARTMENT)
    apply_date = models.DateTimeField(auto_now=True)
    fav_sports = models.CharField(max_length=50)
    interest = models.CharField(max_length=50)
