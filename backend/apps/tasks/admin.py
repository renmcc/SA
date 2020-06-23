from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import updateSystemDate

# Register your models here.


@admin.register(updateSystemDate)
class updateSystemDateAdmin(admin.ModelAdmin):
    list_display =  ['id', 'project', 'region', 'area', 'role', 'servers', 'datetime', 'user', 'taskId', 'channelName', 'add_time']
    # 排序方式 -为倒序
    ordering = ['-id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'project', 'region', 'area', 'role', 'servers', 'datetime']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['project', 'region', 'area']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 10
    # 数据列表页每一页显示最大数
    list_max_show_all = 200
    # 设置可搜索的字段
    search_fields = ['server', 'user']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'update_time'
    # 在数据修改页添加'另存为'功能
    save_as = True