#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/18 0:23
#__author__ = 'ren_mcc'

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .tasks import updateServerDatetime


class updateServerDatetimeConsumer(WebsocketConsumer):
    def connect(self):
        print('connect:', self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({'channel_name': self.channel_name}))

    def disconnect(self, close_code):
        # 中止执行中的Task
        # self.result.revoke(terminate=True)
        print('disconnect:', self.channel_name)

    def receive(self, text_data):
        pass
        # text_data_json = json.loads(text_data)
        # message = '运维咖啡吧：' + text_data_json['message']
        #
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))