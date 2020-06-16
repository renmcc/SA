from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, ProjectRole, ProjectArea, ProjectRegion
from .serializers import ProjectSerializer, ProjectRoleSerializer, ProjectAreaSerializer, ProjectRegionSerializer
from .filter import ProjectFilter, ProjectAreaFilter, ProjectRoleFilter

# Create your views here.


class ProjectView(viewsets.ModelViewSet):
    """
     list:
     返回server列表

     create:
     创建server记录

     retrieve:
     返回server记录

     destroy
     删除server记录

     update:
     更新server记录
     """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    filter_class = ProjectFilter
    filter_fields = ("name", )


class ProjectRoleView(viewsets.ModelViewSet):
    """
     list:
     返回server列表

     create:
     创建server记录

     retrieve:
     返回server记录

     destroy
     删除server记录

     update:
     更新server记录
     """
    queryset = ProjectRole.objects.all()
    serializer_class = ProjectRoleSerializer

    filter_class = ProjectRoleFilter
    filter_fields = ("name", )


class ProjectAreaView(viewsets.ModelViewSet):
    """
     list:
     返回server列表

     create:
     创建server记录

     retrieve:
     返回server记录

     destroy
     删除server记录

     update:
     更新server记录
     """
    queryset = ProjectArea.objects.all()
    serializer_class = ProjectAreaSerializer

    filter_class = ProjectAreaFilter
    filter_fields = ("name", )


class ProjectRegionView(viewsets.ModelViewSet):
    """
     list:
     返回server列表

     create:
     创建server记录

     retrieve:
     返回server记录

     destroy
     删除server记录

     update:
     更新server记录
     """
    queryset = ProjectRegion.objects.all()
    serializer_class = ProjectRegionSerializer
    filter_fields = ("name", )