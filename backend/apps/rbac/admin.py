from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
from . import models

# Register your models here.


# 修改title和header
admin.site.site_title = 'SA后台管理'
admin.site.site_header = 'SA运维管理后台'


@admin.register(models.UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display =  ['id', 'username', 'name', 'mobile', 'email', 'avatar', 'position', 'is_staff', 'is_active',  'date_joined']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'username', 'position', 'mobile', 'email']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['username','name', 'mobile', 'date_joined']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 数据列表页每一页显示最大数
    list_max_show_all = 200
    # 设置可搜索的字段
    search_fields = ['username', 'name', 'mobile']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'date_joined'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'avatar', 'mobile', 'email', 'position',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.GroupProfile)
class GroupProfileAdmin(GroupAdmin):
    list_display =  ['id', 'name', 'add_time', 'update_time']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'name']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['name']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 数据列表页每一页显示最大数
    list_max_show_all = 200
    # 设置可搜索的字段
    search_fields = ['name']
