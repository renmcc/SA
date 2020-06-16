#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/3/8 15:23
#__author__ = 'ren_mcc'

from rest_framework import serializers
from .models import Project, ProjectArea, ProjectRole


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectArea
        fields = '__all__'


class ProjectRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRole
        fields = '__all__'


class ProjectRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRole
        fields = '__all__'


