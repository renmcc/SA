#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/18 0:18
#__author__ = 'ren_mcc'

from django.urls import path
from tasks import consumers

websocket_urlpatterns = [
    path('tasks/updateServerDatetime/', consumers.updateServerDatetimeConsumer),
]