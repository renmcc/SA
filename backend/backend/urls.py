"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()


from rbac.router import rbacRouter
from book.router import bookRouter

router.registry.extend(rbacRouter.registry)
router.registry.extend(bookRouter.registry)

urlpatterns = [
    path('', admin.site.urls),
    # # jwt token
    # path('api-jwt-auth/', obtain_jwt_token),
    path('api/', include((router.urls, 'rest_framework'), namespace='api')),
    path('api-auth', include("rest_framework.urls")),
    path('docs/', include_docs_urls("运维接口文档")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
