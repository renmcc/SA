from django.db import models
from datetime import datetime
from project.models import Project, ProjectRole, ProjectArea, ProjectRegion


# Create your models here.


class server(models.Model):
    region = models.ForeignKey(ProjectRegion, on_delete=models.SET_NULL, blank=True, null=True, related_name='server_region', verbose_name="区域", help_text='区域')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='server_project', verbose_name="项目", help_text='项目')
    area = models.ForeignKey(ProjectArea, on_delete=models.SET_NULL,blank=True, null=True, related_name='server_area',verbose_name="大区", help_text='所属大区')
    role = models.ManyToManyField(ProjectRole, blank=True, related_name='server_role', verbose_name="功能", help_text='功能')
    # role = models.ForeignKey(ProjectRole, on_delete=models.SET_NULL, related_name='server_role', verbose_name="功能", help_text='功能', default=1)
    hostname = models.CharField('主机名', max_length=200, help_text='主机名',blank=True)
    public_ip = models.GenericIPAddressField('外网IP', help_text='外网IP',blank=True, null=True)
    private_ip = models.GenericIPAddressField('内网IP', unique=True, help_text='内网IP')
    os = models.CharField("操作系统", max_length=100, default=None, help_text="操作系统",blank=True)
    cpu = models.CharField("CPU信息", max_length=250, default=None, help_text="CPU信息",blank=True)
    memory = models.CharField("内存信息", max_length=100, default=None, help_text="内存信息",blank=True)
    disk = models.CharField("硬盘信息", max_length=300, null=True, help_text="硬盘信息", blank=True)
    status = models.BooleanField('启用', default=True, help_text='是否启用')
    remark = models.TextField("备注", null=True, help_text="备注",blank=True)
    add_time = models.DateTimeField(default=datetime.now, help_text='添加时间', verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')

    def __str__(self):
        return self.private_ip

    class Meta:
        ordering = ('id',)
        verbose_name = '服务器列表'
        verbose_name_plural = '服务器列表'

    @property
    def regionInfo(self):
        return {'id': self.region.id, 'name': self.region.name} if self.region else {'id': '', 'name': ''}
    @property
    def projectInfo(self):
        return {'id': self.project.id, 'name': self.project.name} if self.project else {'id': '', 'name': ''}

    @property
    def areaInfo(self):
        return {'id': self.area.id, 'name': self.area.name} if self.area else {'id': '', 'name': ''}

    @property
    def roleInfo(self):
        serverObj = server.objects.get(id=self.pk)
        role = serverObj.role.all()
        return [x.name for x in role if role]