#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/11 15:36
#__author__ = 'ren_mcc'

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import server
from .serializers import serverSerializer, celerytaskresultSerializer ,flushcmdbSerializer
from .filter import ServerFilter, celerytaskresultFilter
from .tasks import flushCMDB
from django_celery_results.models import TaskResult
# Create your views here.


class ServerApiView(viewsets.ModelViewSet):
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
    filter_fields = ("private_ip", "public_ip", )


from rest_framework.permissions import DjangoModelPermissions


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


class flushcmdbView(viewsets.GenericViewSet):
    """
     create:
     创建server记录
     """
    serializer_class = flushcmdbSerializer

    def create(self, request):
        res = request.data
        celeryobj = flushCMDB.delay(res['hosts'])
        print(celeryobj)
        result = {
            'task_id': celeryobj.task_id,
            'status': celeryobj.status
        }
        return Response(result)




