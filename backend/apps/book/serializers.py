#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 11:13
__author__ = 'ren_mcc'

from rest_framework import serializers
from . import models


class uploadBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.uploadBook
        fields = '__all__'