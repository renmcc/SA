#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 11:13
__author__ = 'ren_mcc'

# Create your views here.

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler, jwt_decode_handler, jwt_get_username_from_payload
from utils.basic import SaResponse, SaViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.response import Response
from django.contrib.auth.models import Permission
from rest_framework import permissions
from . import serializers
from . import models
from . import filter
import time


class UserAuthView(SaViewSet):
    """
    用户认证获取token
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = serializers.userAuthSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        username = serializer.initial_data.get('username')
        password = serializer.initial_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            return SaResponse({'token': jwt_encode_handler(payload)}, status=status.HTTP_200_OK)
        else:
            return SaResponse('用户认证失败', status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(viewsets.ModelViewSet):
    """
    用户信息接口
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserInfoSerializer
    filter_class = filter.UserFilter
    search_fields = ['name', 'username', 'mobile', 'position', 'is_active']
    lookup_field = 'username'


class ChangePasswordView(SaViewSet):
    """
    修改用户密码接口
    """
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        old_password = serializer.initial_data.get('old_password')
        new_password = serializer.initial_data.get('new_password1')
        if not request.user.check_password(old_password):
            return SaResponse({"password_error": '旧密码输入错误'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        request.user.set_password(new_password)
        request.user.save()
        return SaResponse({'change_password': '密码修改成功'}, status=status.HTTP_200_OK)


class UserGroupsView(viewsets.ModelViewSet):
    """
    用户组接口
    """
    queryset = models.GroupProfile.objects.all()
    serializer_class = serializers.UserGroupsSerializer
    filter_class = filter.UserGroupFilter
    search_fields = ['name']
    lookup_field = 'name'


class PermissionsInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    查询所有权限接口
    """
    pagination_class = None
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionsInfoSerializer
    search_fields = ['name']