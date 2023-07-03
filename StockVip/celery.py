"""
@author: 技术-小明
@time: 2019-04-14 12:54:05
@file: celery.py
@desc:
"""

from datetime import timedelta
from celery.schedules import crontab

import djcelery

djcelery.setup_loader()

# 配置多个队列
CELERY_QUEUES = {
    # 定时任务队列
    'beat_tasks': {
        'exchange': 'beat_tasks',
        'exchange_type': 'direct',
        'binding_key': 'beat_tasks'
    },
    # 普通对列，跑普通任务的队列
    'work_queue': {
        'exchange': 'work_queue',
        'exchange_type': 'direct',
        'binding_key': 'work_queue'
    }
}

CELERY_DEFAULT_QUEUE = 'work_queue'

CELERY_IMPORTS = (
    'apps.mosaic.tasks',
)

CELERY_TIMEZONE = 'Asia/Shanghai'

# 有些情况可以防止死锁
CELERYD_FORCE_EXECV = True

# 设置并发的worker数量
CELERYD_CONCURRENCY = 4

# 允许重试
CELERY_ACKS_LATE = True

# 每个worker最多执行100个任务被销毁，可以防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 100

# 单个任务的最大运行时间
CELERYD_TASK_TIME_LIMIT = 12 * 30

# 定时任务
CELERYBEAT_SCHEDULE = {
    'task1': {
        'task': 'update-cache',  # 任务名称
        'schedule': timedelta(seconds=10),
        'options': {
            'queue': 'beat_tasks'
        }
    },
    'task2': {
        'task': 'update-db',  # 任务名称
        'schedule': crontab(minute=0, hour=0),
        'options': {
            'queue': 'beat_tasks'
        }
    }
}

# 定时任务
# CELERYBEAT_SCHEDULE = {
#     'task1': {
#         'task': 'demo-task',  # 任务名称
#         'schedule': timedelta(seconds=5),
#         'options': {
#             'queue': 'beat_tasks'
#         }
#     }
# }