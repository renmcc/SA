#!/usr/bin/env python
#coding:utf8
#__time__:2019/8/1212:09
#__author__:"ren_mcc"

import django_filters
from .models import server
from django_celery_results.models import TaskResult
from django.db.models import Q


class ServerFilter(django_filters.rest_framework.FilterSet):
    '''server接口过滤'''
    # regionInfo = django_filters.CharFilter(field_name='regionInfo', help_text="地区模糊查询", lookup_expr='icontains')
    update_time = django_filters.DateTimeFromToRangeFilter(field_name='update_time', help_text="更新时间过滤",)

    class Meta:
        model = server
        fields = ["region", 'project', 'area', 'update_time']


class celerytaskresultFilter(django_filters.FilterSet):
    django_filters.CharFilter(method="search_id")

    def search_id(self, queryset, task_id, task_name):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(task_id__icontains=task_id)|Q(task_name__icontains=task_name))

    class Meta:
        model = TaskResult
        fields = ['task_id', 'task_name']