#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 11:13
__author__ = 'ren_mcc'

from rest_framework import serializers
from django.contrib.auth.hashers import check_password
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
        fields = [ 'id',  'username',  'name', 'email', 'is_active', 'date_joined', 'mobile', 'avatar', 'position', 'roles', 'user_permissions', 'groups']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'user_permissions': {
              'read_only': True
            },
            'groups': {
                'write_only': True
            },
            'date_joined': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def validate_username(self, value):
        if models.UserProfile.objects.filter(username=value):
            raise serializers.ValidationError({"usernameError":"用户名已存在"})
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, error_messages={
        'required': '密码不能为空',
    })
    new_password1 = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, min_length=3, error_messages={
        'min_length': '新密码不能少于3个字符',
    })
    new_password2 = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'}, min_length=3, error_messages={
        'min_length': '新密码不能少于3个字符',
    })

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')
        if new_password1 != new_password2:
            raise serializers.ValidationError({'new_password_error': '两次密码不一致'})
        return attrs