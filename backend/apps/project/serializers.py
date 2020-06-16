#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/8 15:23
#__author__ = 'ren_mcc'

from rest_framework import serializers
from .models import Project, ProjectArea, ProjectRole, ProjectRegion


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'created': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }



class ProjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectArea
        fields = '__all__'
        extra_kwargs = {
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'created': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }


class ProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRole
        fields = '__all__'
        extra_kwargs = {
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'created': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }


class ProjectRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRegion
        fields = ['id', 'name', 'remark', 'created', 'update_time']
        extra_kwargs = {
            'update_time': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'created': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            },
        }


