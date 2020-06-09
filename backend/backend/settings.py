"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&2#ixu2i0)01=licu+htts6fh%=iap2si&(+7^rw4lk!*+)sq$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'import_export',
    'rbac.apps.RbacConfig',
    'book.apps.BookConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "SA2",
        'USER': 'root',
        'PASSWORD': "123456",
        'HOST': "192.168.10.10",
        'PORT': "3306",
        'OPTIONS': {
            'init_command': "SET storage_engine=INNODB;SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = 'rbac.UserProfile'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    # docs用
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 全局解析类配置    url拼接参数，数据包参数：form-data,urlencoding,json
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    # 添加token认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    # 分页
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.DefaultPagination",
    # 搜索
    'DEFAULT_FILTER_BACKENDS': (
        # 字段过滤
        'django_filters.rest_framework.DjangoFilterBackend',
        # 搜索
        'rest_framework.filters.SearchFilter',
        # 排序
        'rest_framework.filters.OrderingFilter',
    ),

}


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=5),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


# 缓存过期时间
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 5
}



# simpleui 设置
# 首页配置
# SIMPLEUI_HOME_PAGE = 'https://www.baidu.com'
# 首页标题
# SIMPLEUI_HOME_TITLE = '百度一下你就知道'
# 首页图标,支持element-ui的图标和fontawesome的图标
# SIMPLEUI_HOME_ICON = 'el-icon-date'

# 设置simpleui 点击首页图标跳转的地址
# SIMPLEUI_INDEX = 'https://www.88cto.com'

# 首页显示服务器、python、django、simpleui相关信息
SIMPLEUI_HOME_INFO = False

# 首页显示快速操作
# SIMPLEUI_HOME_QUICK = False

# 首页显示最近动作
# SIMPLEUI_HOME_ACTION = False

# 自定义SIMPLEUI的Logo
# SIMPLEUI_LOGO = 'https://avatars2.githubusercontent.com/u/13655483?s=60&v=4'

# 登录页粒子动画，默认开启，False关闭
SIMPLEUI_LOGIN_PARTICLES = False

# 让simpleui 不要收集相关信息
SIMPLEUI_ANALYSIS = False

# 自定义simpleui 菜单
SIMPLEUI_CONFIG = {
    # 在自定义菜单的基础上保留系统模块
    'system_keep': True,
    'menu_display':  ['图书管理', '用户管理'],
    'menus': [
        {
            'name': 'API',
            'icon': 'fas fa-file-code',
            'models': [
                {
                'name': 'api接口',
                'url': '/api/',
                'icon': 'fas fa-file-code'
                },
                {
                    'name': 'api接口文档',
                    'url': '/docs/',
                    'icon': 'fas fa-file-code'
                },
            ]
        },
        {
            'name': '测试',
            'icon': 'fas fa-file-code',
            'models': [
                {
                    'name': '百度',
                    'url': 'https://www.baidu.com',
                    'icon': 'fas fa-file-code'
                },
                {
                    'name': '测试',
                    'url': '/api/server/',
                    'icon': 'fas fa-file-code'
                },
                {
                    'name': '测试服务器接口',
                    'url': '/api/cmdb_celerytaskresult/?format=json',
                    'icon': 'fas fa-file-code'
                },
            ]
        },
    ]
}

# 是否显示默认图标，默认=True
# SIMPLEUI_DEFAULT_ICON = False

# 图标设置，图标参考：
SIMPLEUI_ICON = {
    '服务器管理': 'fas fa-server',
    '项目管理': 'fab fa-elementor',
}



# 指定simpleui 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目
# 不填该项或者为False的时候，默认从第三方的cdn获取

SIMPLEUI_STATIC_OFFLINE = True