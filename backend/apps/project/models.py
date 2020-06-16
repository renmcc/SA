from django.db import models
from datetime import datetime
# Create your models here.


class ProjectArea(models.Model):
    name = models.CharField('项目大区', max_length=50, unique=True, help_text='项目大区', default='未分配')
    remark = models.TextField("备注", null=True, blank=True, help_text="备注")
    created = models.DateTimeField(auto_now=True, help_text='创建时间', verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        ordering = ('id',)
        verbose_name = '项目大区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField('项目名称', max_length=50, unique=True, help_text="项目名称", default='未分配')
    remark = models.TextField("备注", null=True, blank=True, help_text="备注")
    created = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        ordering = ('id',)
        verbose_name = '项目名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProjectRole(models.Model):
    name = models.CharField('项目角色', max_length=50, unique=True, help_text='项目角色', default='未分配')
    remark = models.TextField("备注", null=True, blank=True, help_text="备注")
    created = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        ordering = ('id',)
        verbose_name = '项目角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProjectRegion(models.Model):
    name = models.CharField('区域', max_length=50, unique=True, help_text='项目角色', default='区域')
    remark = models.TextField("备注", null=True, help_text="备注")
    created = models.DateTimeField('创建时间', auto_now=True, help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    class Meta:
        ordering = ('id',)
        verbose_name = '区域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


