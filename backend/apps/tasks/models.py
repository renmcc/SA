from django.db import models
from datetime import datetime
from mdeditor.fields import MDTextField
# Create your models here.

class updateSystemDate(models.Model):
    project = models.CharField(max_length=255, verbose_name="项目", help_text='项目')
    region = models.CharField(max_length=255, verbose_name="区域", help_text='区域')
    area = models.CharField(max_length=255, verbose_name="大区", help_text='大区')
    role = models.CharField(max_length=255, verbose_name="角色", help_text='角色')
    servers = models.CharField(max_length=255, verbose_name="服务器IP", help_text='服务器IP')
    channelName = models.CharField(max_length=255, verbose_name="channelName", help_text='channelName')
    datetime = models.CharField(max_length=255, help_text='更新系统时间', verbose_name='更新系统时间')
    taskId = models.CharField(max_length=255, verbose_name="任务ID", help_text='任务ID')
    user = models.CharField(max_length=255, verbose_name="操作用户", help_text='操作用户')
    results = MDTextField(default='', verbose_name="任务结果", help_text='任务结果')
    add_time = models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        verbose_name = "更新服务器时间"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return '%s time is %s' % (self.servers, self.datetime)