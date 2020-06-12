#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/9 15:42
#__author__ = 'ren_mcc'

import django_filters
from .models import UserProfile, GroupProfile
from django.db.models import Q


class UserFilter(django_filters.rest_framework.FilterSet):
    '''用户信息过滤'''
    name = django_filters.CharFilter(field_name='name', help_text="用户名模糊查询", lookup_expr='icontains')
    date_joined = django_filters.DateTimeFromToRangeFilter(field_name='date_joined', help_text="按创建时间过滤",)

    class Meta:
        model = UserProfile
        fields = ["name", 'date_joined']


class UserGroupFilter(django_filters.rest_framework.FilterSet):
    '''用户组信息过滤'''
    name = django_filters.CharFilter(field_name='name', help_text="用户组模糊查询", lookup_expr='icontains')
    add_time = django_filters.DateTimeFromToRangeFilter(field_name='add_time', help_text="按创建时间过滤",)

    class Meta:
        model = GroupProfile
        fields = ["name", 'add_time']