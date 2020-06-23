#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/6/18 22:39
#__author__ = 'ren_mcc'
import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,project_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

from celery import states
from celery.result import AsyncResult
from celery.utils import get_full_cls_name
from celery.utils.encoding import safe_repr



result = AsyncResult('e27afabf-06c2-4131-98bf-ffcf12720597')
print(result.state, result.result)