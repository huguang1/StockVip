"""
Django settings for StockVip project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, BASE_DIR)
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qtf^-ipr@jsyh5^dh@(yu6-ubm)4*b386je@k^bj+=i)8hqmp7'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'system.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.system',
    'apps.stock',
    'apps.member',
    'apps.mosaic',
    'apps.index',
    'djcelery'
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

ROOT_URLCONF = 'StockVip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'front/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.system.context_processors.front_user'
            ],
            'builtins': [
                'django.templatetags.static'
            ]
        },
    },
]

WSGI_APPLICATION = 'StockVip.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'stockvip',
#         'USER': 'root',
#         'PASSWORD': 'mpo{qczj4nIzyAr6',
#         'PORT': '3306',
#         'HOST': '103.94.77.31',
#         'OPTIONS': {
#             'init_command': 'SET default_storage_engine=INNODB;',
#             'charset': 'utf8'
#         }
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stockvip',
        'USER': 'root',
        'PASSWORD': 'Hdug&34dg1Gd',
        'PORT': '3306',
        'HOST': '192.168.29.165',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB;',
            'charset': 'utf8'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# SESSION_COOKIE_SECURE = True
# CSRF_USE_SESSIONS = True

LOGIN_URL = "/system/login/"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

USE_I18N = True

USE_L10N = True

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front/dist')
]
# STATIC_ROOT = '/var/www/static/stockvip/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'front/media')
# MEDIA_ROOT = '/var/www/media/stockvip/'

# 分页配置,每页显示多少条数据
PAGE_COUNT = 15

# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.29.165:6379/8",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:p4GI7vxlbkm-aufx@localhost:6379/12",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#             "IGNORE_EXCEPTIONS": True,
#         }
#     }
# }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 日志
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")

LOGGING = {
    'version': 1,  # 保留的参数，默认是1
    'disable_existing_loggers': False,  # 是否禁用已经存在的logger实例
    # 日志输出格式的定义
    'formatters': {
        'standard': {  # 标准的日志格式化
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'error': {  # 错误日志输出格式
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    # 处理器：需要处理什么级别的日志及如何处理
    'handlers': {
        # 将日志打印到终端
        'console': {
            'level': 'DEBUG',  # 日志级别
            'class': 'logging.StreamHandler',  # 使用什么类去处理日志流
            'formatter': 'simple'  # 指定上面定义过的一种日志输出格式
        },
        # 默认日志处理器
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "stockvip.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志输出格式
            'encoding': 'utf-8',
        },
        # 日志处理级别warn
        'warn': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "warn.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志格式
            'encoding': 'utf-8',
        },
        # 日志级别error
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "error.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,
            'formatter': 'error',  # 日志格式
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        # 默认的logger应用如下配置
        'django': {
            'handlers': ['default', 'warn', 'error'],
            'level': 'DEBUG',
            'propagate': True,  # 如果有父级的logger示例，表示不要向上传递日志流
        },
        'collect': {
            'handlers': ['console', 'default', 'warn', 'error'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['default', 'error', 'warn'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}

# 调试工具配置
# if DEBUG:
#     INTERNAL_IPS = ("127.0.0.1",)
#     DEBUG_TOOLBAR_PANELS = [
#         # 代表是哪个django版本
#         'debug_toolbar.panels.versions.VersionsPanel',
#         # 用来计时的，判断加载当前页面总共花的时间
#         'debug_toolbar.panels.timer.TimerPanel',
#         # 读取django中的配置信息
#         'debug_toolbar.panels.settings.SettingsPanel',
#         # 看到当前请求头和响应头信息
#         'debug_toolbar.panels.headers.HeadersPanel',
#         # 当前请求的想信息（视图函数，Cookie信息，Session信息等）
#         'debug_toolbar.panels.request.RequestPanel',
#         # 查看SQL语句
#         'debug_toolbar.panels.sql.SQLPanel',
#         # 静态文件
#         'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#         # 模板文件
#         'debug_toolbar.panels.templates.TemplatesPanel',
#         # 缓存
#         'debug_toolbar.panels.cache.CachePanel',
#         # 信号
#         'debug_toolbar.panels.signals.SignalsPanel',
#         # 日志
#         'debug_toolbar.panels.logging.LoggingPanel',
#         # 重定向
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ]
#
#     DEBUG_TOOLBAR_CONFIG = {
#         'JQUERY_URL': '/static/js/jquery-3.3.1.min.js'
#     }
#
#     MIDDLEWARE += (
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#
#     )
#
#     INSTALLED_APPS += (
#         'debug_toolbar',
#     )

# Celery
from .celery import *

BROKER_BACKEND = 'redis'
BROKER_URL = 'redis://192.168.29.165:6379/9'
CELERY_RESULT_BACKEND = 'redis://192.168.29.165:6379/10'
