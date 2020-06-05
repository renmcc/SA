#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 11:13
__author__ = 'ren_mcc'

from rest_framework import serializers
from . import models


class userAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, write_only=True,
                                     error_messages={
                                         'max_length': '用户名不能超过10个字符',
                                     })
    password = serializers.CharField(max_length=20, style={'input_type': 'password'}, write_only=True,
                                    error_messages={
                                        'max_length': '密码不能超过20个字符',
                                    })





class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['id', 'username', 'email', 'is_active', 'date_joined', 'mobile', 'avatar', 'name', 'position', 'roles', 'user_permissions']