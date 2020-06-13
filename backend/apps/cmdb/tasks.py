#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/5 19:26
#__author__ = 'ren_mcc'

from backend import celery_app as app
from utils.ansibleApi import ANSRunner
import datetime
import time



@app.task
def flushCMDB(hosts='all'):
    currentdate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rediskey = "flushcmdb-%s" % currentdate
    tasks = []
    tasks.append(dict(action=dict(module='setup')))
    obj = ANSRunner()
    obj.runner(rediskey, hosts, tasks)
    return obj.get_result()

