#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/8 15:23
#__author__ = 'ren_mcc'

from rest_framework import serializers
from . import models


class updateSystemDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.updateSystemDate
        fields = ['id', 'project', 'region', 'area', 'role', 'servers', 'datetime', 'user', 'channelName', 'taskId', 'results', 'add_time', 'update_time']
        extra_kwargs = {
            'time': {
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'results': {
                'required': False,
            },
            'taskId': {
                'read_only': True,
            },
            'user': {
                'read_only': True,
            },
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'add_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }
