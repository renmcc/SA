#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/5 19:13
#__author__ = 'ren_mcc'
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 注册Celery的APP
app = Celery('backend')
# 设置时区
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False
# 添加下面两行
app.conf.task_send_sent_event = True
app.conf.worker_send_task_events = True
app.conf.broker_url = 'redis://192.168.10.10:6379/8'
app.conf.result_backend = 'django-db'
app.conf.result_serializer = 'json'
app.conf.force_execv = True

# 绑定配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现各个app下的tasks.py文件
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


