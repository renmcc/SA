#!/usr/bin/env python
#coding:utf-8
#__time__: 2020/4/8 16:00
#__author__ = 'ren_mcc'

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# 调用 ansible-doc 时可见，同时“声明”插件需要的选项以及如何配置它们。
DOCUMENTATION = '''
  callback: timer
  callback_type: aggregate
  requirements:
    - whitelist in configuration
  short_description: Adds time to play stats
  version_added: "2.0"
  description:
      - This callback just adds total play duration to the play stats.
  options:
    format_string:
      description: format of the string shown to user at play end
      ini:
        - section: callback_timer
          key: format_string
      env:
        - name: ANSIBLE_CALLBACK_TIMER_FORMAT
      default: "Playbook run took %s days, %s hours, %s minutes, %s seconds"
'''
from datetime import datetime
from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    """
    这个插件会输出任务执行时间
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'timer'

    # 这个参数会要求在 ansible 配置文件中 whitelist 启用
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        # 确保调用 __init__
        super(CallbackModule, self).__init__()

        # 记录当前时间
        self.start_time = datetime.now()

    def _days_hours_minutes_seconds(self, runtime):
        '''内部方法，将时间格式化 '''
        minutes = (runtime.seconds // 60) % 60
        r_seconds = runtime.seconds - (minutes * 60)
        return runtime.days, runtime.seconds // 3600, minutes, r_seconds

    # ansible 执行有多个事件，这里只关注这一个
    def v2_playbook_on_stats(self, stats):
        end_time = datetime.now()
        runtime = end_time - self.start_time

        # 在任务结束后显示执行消耗的时间
        self._display.display(self._plugin_options['format_string'] % (self._days_hours_minutes_seconds(runtime)))