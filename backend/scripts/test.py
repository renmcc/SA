#!/usr/bin/env python
#coding:utf8
#__time__:2019/8/2017:24
#__author__:"ren_mcc"

# import json
#
# with open("aaa.json", "r") as f:
#     data = json.dumps(f.read())

# import subprocess
# # ret = subprocess.Popen('export ANSIBLE_CONFIG=/data/github/SA2/backend/tools/ansible.cfg; python -V; ansible-playbook /data/github/SA2/backend/tools/playbooks/test.yml', shell=True, stdout=subprocess.PIPE)
# #
# # for line in iter(ret.stdout.readline, b''):
# #     print(line.decode())
# # ret.stdout.close()
# # ret.wait()

import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,project_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
#
# def updateServerDatetime():
#     channel_layer = get_channel_layer()
#
#     async_to_sync(channel_layer.send)(
#         'specific.fBjVDUEn!WwqqPxJaCcEf',
#         {
#             "type": "send_message",
#             "message": 'eeeeeeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaaa'
#         }
#     )
#
# updateServerDatetime()

