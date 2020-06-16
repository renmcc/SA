from rest_framework.routers import DefaultRouter
from .views import ProjectView, ProjectRoleView, ProjectAreaView, ProjectRegionView


projectRouter = DefaultRouter()
projectRouter.register(r'project', ProjectView, basename="project")
projectRouter.register(r'projectRole', ProjectRoleView, basename="projectRole")
projectRouter.register(r'projectArea', ProjectAreaView, basename="projectArea")
projectRouter.register(r'projectRegion', ProjectRegionView, basename="projectRegion")



