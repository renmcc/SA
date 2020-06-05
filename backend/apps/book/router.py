from rest_framework.routers import DefaultRouter
from . import views


bookRouter = DefaultRouter()
bookRouter.register(r'uploadBook', views.uploadBookViewSet, basename="uploadBook")


