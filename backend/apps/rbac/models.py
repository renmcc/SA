from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from datetime import datetime


# Create your models here.


class UserProfile(AbstractUser):
    """用户"""
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    image = models.ImageField(upload_to="static/%Y/%m", default="image/default.png",
                              max_length=100, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username


class GroupProfile(Group):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField('更新时间', auto_now=True, help_text='更新时间')

    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = verbose_name