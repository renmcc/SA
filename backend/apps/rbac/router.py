from rest_framework.routers import DefaultRouter
from . import views


rbacRouter = DefaultRouter()
rbacRouter.register(r'userAuth', views.UserAuthView, basename="userAuth")
rbacRouter.register(r'userInfo', views.UserInfoView, basename="userInfo")
rbacRouter.register(r'changePassword', views.ChangePasswordView, basename="changePassword")
rbacRouter.register(r'groupsInfo', views.UserGroupsView, basename="groupsInfo")
rbacRouter.register(r'permissionsInfo', views.PermissionsInfoView, basename="permissionsInfo")


