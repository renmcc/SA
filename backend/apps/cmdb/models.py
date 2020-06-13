from django.db import models

# Create your models here.


class server(models.Model):
    AREA = (
        ('0', '未分配'),
        ('101', '测试大区'),
        ('102', '提审大区'),
        ('103', '预发布大区'),
        ('104', '正式大区')
    )
    PROJECT = (
        ('未分配','未分配'),
        ('王者荣耀','王者荣耀'),
        ('和平精英','和平精英')
    )
    ROLE = (
        ('未分配', '未分配'),
        ('login', 'login'),
        ('idip', 'idip'),
        ('game', 'game'),
        ('match', 'match'),
        ('battlematch', 'battlematch'),
        ('battle', 'battle'),
    )
    area = models.CharField('大区', max_length=50, choices=AREA, default='0', help_text='大区')
    project = models.CharField('项目', max_length=50, choices=PROJECT, default='空闲', help_text='项目')
    role = models.CharField('功能', max_length=50, choices=ROLE, default='空闲', help_text='功能')
    hostname = models.CharField('主机名', max_length=200, help_text='主机名',blank=True)
    public_ip = models.GenericIPAddressField('外网IP', help_text='外网IP',blank=True, null=True)
    private_ip = models.GenericIPAddressField('内网IP', unique=True, help_text='内网IP')
    os = models.CharField("操作系统", max_length=100, default=None, help_text="操作系统",blank=True)
    cpu = models.CharField("CPU信息", max_length=250, default=None, help_text="CPU信息",blank=True)
    memory = models.CharField("内存信息", max_length=100, default=None, help_text="内存信息",blank=True)
    disk = models.CharField("硬盘信息", max_length=300, null=True, help_text="硬盘信息", blank=True)
    status = models.BooleanField('启用', default=False, help_text='是否启用')
    remark = models.TextField("备注", null=True, help_text="备注",blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, help_text='更新时间')

    def __str__(self):
        return self.private_ip

    class Meta:
        ordering = ('id',)
        verbose_name = '服务器列表'
        verbose_name_plural = '服务器列表'