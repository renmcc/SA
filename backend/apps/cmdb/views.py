#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/11 15:36
#__author__ = 'ren_mcc'

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django_celery_results.models import TaskResult
from utils.basic import SaViewSet, SaResponse
from rest_framework import permissions, status
from .models import server
from .serializers import serverSerializer, celerytaskresultSerializer ,flushcmdbSerializer
from .filter import ServerFilter, celerytaskresultFilter
from . import tasks

# Create your views here.


class serverInfoView(viewsets.ModelViewSet):
    """
     list:
     返回server列表

     create:
     创建server记录

     retrieve:
     返回server记录

     destroy
     删除server记录

     update:
     更新server记录
     """
    queryset = server.objects.all()
    serializer_class = serverSerializer
    filter_class = ServerFilter
    search_fields = ['private_ip', 'public_ip']



class celerytaskresultView(viewsets.ReadOnlyModelViewSet):
    """
    list:
    获取celery任务结果

    retrieve:
    获取指定celery任务结果

    """
    queryset = TaskResult.objects.all()
    serializer_class = celerytaskresultSerializer
    filter_class = celerytaskresultFilter


class flushcmdbView(SaViewSet):
    """
     create:
     创建server记录
     """
    serializer_class = flushcmdbSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        host = serializer.initial_data.get('host')
        res = tasks.flushCMDB.delay(host)
        return SaResponse(res.task_id, status=status.HTTP_200_OK)






