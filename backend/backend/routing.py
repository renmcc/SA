#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/17 20:50
#__author__ = 'ren_mcc'
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tasks.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tasks.routing.websocket_urlpatterns
        )
    ),
})