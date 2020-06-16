#!/usr/bin/env python
#coding:utf8
#__time__:2019/8/1212:09
#__author__:"ren_mcc"

import django_filters
from .models import Project, ProjectRole, ProjectArea
from django.db.models import Q


class ProjectFilter(django_filters.FilterSet):
    search_name = django_filters.CharFilter(method="search_name")

    def search_name(self, queryset, name, value):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(name__icontains=value)|Q(name__icontains=value))

    class Meta:
        model = Project
        fields = ['name', ]


class ProjectRoleFilter(django_filters.FilterSet):
    search_name = django_filters.CharFilter(method="search_name")

    def search_name(self, queryset, name, value):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(name__icontains=value)|Q(name__icontains=value))

    class Meta:
        model = ProjectRole
        fields = ['name', ]


class ProjectAreaFilter(django_filters.FilterSet):
    search_name = django_filters.CharFilter(method="search_name")

    def search_name(self, queryset, name, value):
        # 通过Q实现多条件搜索
        return queryset.filter(Q(name__icontains=value)|Q(name__icontains=value))

    class Meta:
        model = ProjectArea
        fields = ['name', ]


