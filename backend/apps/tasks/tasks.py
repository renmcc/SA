#!/opt/pyenv/versions/SA2/bin/python
#coding:utf-8
#__time__: 2020/4/5 19:26
#__author__ = 'ren_mcc'

from backend import celery_app as app
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
import subprocess
from .models import updateSystemDate


@app.task
def updateServerDatetime(channel_name, servers, datetime):
    cmd =  '/opt/pyenv/versions/SA2/bin/ansible {0}  -m shell -a "date -s \'{1}\'"'.format(servers, datetime)
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    channel_layer = get_channel_layer()
    data = ''
    for line in iter(ret.stdout.readline, b''):
        async_to_sync(channel_layer.send)(
            channel_name,
            {
                "type": "send_message",
                "message": line.decode()
            }
        )
        data += line.decode()
    ret.stdout.close()
    ret.wait()
    taskid = updateServerDatetime.request.id
    querySet = updateSystemDate.objects.get(taskId=taskid)
    querySet.results = data
    querySet.save()
    return data