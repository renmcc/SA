#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/5 19:26
#__author__ = 'ren_mcc'

from backend import celery_app as app
from utils.ansibleApi import ANSRunner
import datetime
import time
from .models import server
import json



@app.task
def flushCMDB(hosts='all'):
    currentdate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rediskey = "flushcmdb-%s" % currentdate
    tasks = []
    tasks.append(dict(action=dict(module='setup')))
    obj = ANSRunner()
    obj.runner(rediskey, hosts, tasks)
    hostDatas = obj.get_result()['ok']
    serversQuerysets = server.objects.all()
    for serversQueryset in serversQuerysets:
        hostdata = hostDatas.get(serversQueryset.private_ip)
        if hostdata:
            facts = hostdata['ansible_facts']
            serversQueryset.hostname = facts['ansible_nodename']
            serversQueryset.os = facts['ansible_os_family']
            serversQueryset.cpu = '%s-%s' %(facts['ansible_processor_vcpus'], facts['ansible_processor'][2])
            serversQueryset.memory = '%sMB' % facts['ansible_memtotal_mb']
            serversQueryset.disk = facts['ansible_devices']['sda']['size']
            serversQueryset.save()
