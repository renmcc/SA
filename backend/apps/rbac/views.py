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
from . import serializers
from . import models


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


class UserInfoView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取当前用户信息和权限
    """
    serializer_class = serializers.UserInfoSerializer

    def get_queryset(self):
        return models.UserProfile.objects.filter(username=self.request.user)
