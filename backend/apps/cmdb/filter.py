#!/usr/bin/env python
#coding:utf8
#__time__:2019/8/1212:09
#__author__:"ren_mcc"

import django_filters
from .models import server
from django_celery_results.models import TaskResult
from django.db.models import Q


class ServerFilter(django_filters.FilterSet):
    search_ip = django_filters.CharFilter(method="search_ip")

    def search_ip(self, queryset, value):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(public_ip__icontains=value)|Q(private_ip__icontains=value))

    class Meta:
        model = server
        fields = ['public_ip', 'private_ip']


class celerytaskresultFilter(django_filters.FilterSet):
    django_filters.CharFilter(method="search_id")

    def search_id(self, queryset, task_id, task_name):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(task_id__icontains=task_id)|Q(task_name__icontains=task_name))

    class Meta:
        model = TaskResult
        fields = ['task_id', 'task_name']