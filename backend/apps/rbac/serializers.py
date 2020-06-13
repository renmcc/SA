#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 11:13
__author__ = 'ren_mcc'

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
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
        fields = [ 'id',  'username',  'name', 'password', 'email', 'is_active', 'date_joined', 'mobile', 'avatar', 'position', 'roles', 'user_permissions', 'groups']
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'user_permissions': {
              'read_only': True
            },
            'avatar': {
                'read_only': True
            },
            'password': {
                'style': {'input_type': 'password'}
            },
            'date_joined': {
                'read_only': True,
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def validate_username(self, value):
        if models.UserProfile.objects.filter(username=value):
            raise serializers.ValidationError({"usernameError":"用户名已存在"})
        return value

    def validate_password(self, value):
        if models.UserProfile.objects.filter(password=value):
            return value
        else:
            return make_password(value)


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


class UserGroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.GroupProfile
        fields = ['id', 'name', 'permissions', 'permissions2', 'add_time', 'update_time']
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

    def validate_name(self, value):
        if models.GroupProfile.objects.filter(name=value):
            raise serializers.ValidationError({"nameError":"用户组已存在"})
        return value


class PermissionsInfoSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    class Meta:
        model = queryset = Permission
        fields = ['id', 'label']

    def get_label(selfself, obj):
        return "%s | %s | %s" % (
            obj.content_type.app_label,
            obj.content_type,
            obj.name,
        )