#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/2 0:19
#__author__ = 'ren_mcc'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# 注册一个信号，在创建用户时自动加密密码
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()