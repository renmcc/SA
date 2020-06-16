#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/8 15:23
#__author__ = 'ren_mcc'

from rest_framework import serializers
from .models import  server
from django_celery_results.models import TaskResult

class serverSerializer(serializers.ModelSerializer):

    class Meta:
        model = server
        fields = ['id', 'region', 'regionInfo', 'project', 'projectInfo', 'area', 'areaInfo', 'role', 'roleInfo', 'hostname', 'public_ip', 'private_ip', 'os', 'cpu', 'memory', 'disk', 'status', 'remark', 'add_time', 'update_time']

        extra_kwargs = {
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'add_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }


class celerytaskresultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = '__all__'

class flushcmdbSerializer(serializers.Serializer):
    host = serializers.CharField(required=True, max_length=200, label='执行任务的hosts', help_text='执行任务的hosts')


