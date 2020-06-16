from django.contrib import admin
from .models import Project, ProjectRole, ProjectArea, ProjectRegion

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'created', 'update_time']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'name']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['name',]
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 设置可搜索的字段
    # search_fields = ['name', 'role']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'created'
    # 在数据修改页添加'另存为'功能
    save_as = True


@admin.register(ProjectArea)
class ProjectAreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'created', 'update_time']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'name']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['name']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 设置可搜索的字段
    # search_fields = ['name', 'role']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'created'
    # 在数据修改页添加'另存为'功能
    save_as = True


@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'created', 'update_time']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'name']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['name']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 设置可搜索的字段
    # search_fields = ['name', 'role']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'created'
    # 在数据修改页添加'另存为'功能
    save_as = True


@admin.register(ProjectRegion)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remark', 'created', 'update_time']
    # 排序方式 -为倒序
    ordering = ['id']
    # 为数据列表页的字段id和job设置路由地址，该路由地址可进入数据修改页
    list_display_links = ['id', 'name']
    # 设置过滤器，若有外键，则应该使用双下划线连接两个模型的字段
    list_filter = ['name']
    # 在数据列表页设置每一页显示的数据
    list_per_page = 50
    # 设置可搜索的字段
    # search_fields = ['name', 'role']
    # 在数据列表页设置日期选择器
    date_hierarchy = 'created'
    # 在数据修改页添加'另存为'功能
    save_as = True