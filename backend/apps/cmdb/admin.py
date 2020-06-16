from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import server

# Register your models here.


@admin.register(server)
class ServerAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display =  ['id', 'region', 'project', 'area', 'hostname', 'public_ip', 'private_ip', 'os', 'cpu', 'memory', 'disk', 'remark', 'update_time', 'status']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'hostname', 'private_ip']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['area', 'project']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 10
    # 数据列表页每一页显示最大数
    list_max_show_all = 200
    # 设置可搜索的字段
    search_fields = ['public_ip', 'private_ip']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'update_time'
    # 在数据修改页添加'另存为'功能
    save_as = True
    # 在列表页设置可编辑的字段
    # list_editable =['area', 'project', 'role']

    def _get_cmdb_info(self, private_ip):
        import os
        import json

        jsonfile = '/tmp/facts_cache/%s'% private_ip
        res = {}
        if os.path.isfile(jsonfile):
            with open(jsonfile, encoding='utf-8') as f:
                data = json.load(f)
                res['hostname'] = data['ansible_nodename']
                res['os'] = data['ansible_os_family']
                res['cpu'] = '%s-%s' %(data['ansible_processor_vcpus'], data['ansible_processor'][2])
                res['mem'] = '%sMB' % data['ansible_memtotal_mb']
                res['disk'] = data['ansible_devices']['sda']['size']
        return res


    def flush_cmdb(self, request, queryset):
        for d in queryset:
            res = self._get_cmdb_info(d.private_ip)
            if res:
                d.hostname = res['hostname']
                d.os = res['os']
                d.cpu = res['cpu']
                d.memory = res['mem']
                d.disk = res['disk']
                d.save()

    flush_cmdb.short_description = '刷新资产'
    flush_cmdb.type = 'primary'

    actions = ['export_admin_action', 'flush_cmdb', ]
