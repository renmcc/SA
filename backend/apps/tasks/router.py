from rest_framework.routers import DefaultRouter
from . import views


tasksRouter = DefaultRouter()
tasksRouter.register(r'updateSystemDate', views.updateSystemDateView, basename="updateSystemDate")

