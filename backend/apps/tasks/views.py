from django.shortcuts import render
from utils.basic import SaViewSet, SaResponse
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response
from . import serializers
from . import tasks
from . import models

# Create your views here.


class updateSystemDateView(viewsets.ModelViewSet):
    """更新系统时间"""
    queryset = models.updateSystemDate.objects.all()
    serializer_class = serializers.updateSystemDateSerializer
    search_fields = ['user']
    filter_fields = ['user']

    def create(self, request, *args, **kwargs):
        channelName = str(request.data['channelName'])
        servers = str(request.data['servers'])
        datetime = str(request.data['datetime'])
        resultObj = tasks.updateServerDatetime.delay(channelName, servers, datetime)
        request.data['taskId'] = resultObj.task_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'taskid': resultObj.task_id}, status=status.HTTP_201_CREATED, headers=headers)
