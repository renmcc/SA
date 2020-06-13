#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/8 15:23
#__author__ = 'ren_mcc'

from rest_framework import serializers
from .models import  server
from django_celery_results.models import TaskResult

class serverSerializer(serializers.ModelSerializer):

    # 序列化最后一步
    # def to_representation(self, instance):
    #     ret = super(serverSerializer, self).to_representation(instance)
    #     ret['area'] = {"id": instance.area.id, "name": instance.area.name}
    #     ret['project'] = {"id": instance.project.id, "name": instance.project.name}
    #     ret['role'] = {"id": instance.role.id, "name": instance.role.name}
    #     return ret

    class Meta:
        model = server
        fields = '__all__'


class celerytaskresultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = '__all__'

class flushcmdbSerializer(serializers.Serializer):
    hosts = serializers.CharField(required=True, max_length=200, label='执行任务的hosts', help_text='执行任务的hosts')


