"""
@author: 技术-小明
@time: 2019-04-14 12:51:49
@file: tasks.py
@desc:
"""

import time
import random

from celery.task import Task

from django.core.cache import cache

from apps.mosaic.models import OnlineMember


# class DemoTask(Task):
    # 任务命名
#     name = 'demo-task'

    # 运行任务的函数
#     def run(self, *args, **kwargs):
#         print('start demo task')

#         time.sleep(5)

#         print('args={}, kwargs={}'.format(args, kwargs))

#         print('end demo task')


# 更新缓存
class UpdateCache(Task):
    name = 'update-cache'

    def run(self, *args, **kwargs):
        count = cache.get("online-count-stockvip")
        if not count:
            try:
                data = OnlineMember.objects.get(id=1)
                count = data.people_count
            except:
                count = 800
                OnlineMember.objects.create(people_count=count)

            cache.set(key="online-count-stockvip", value=count, timeout=None)
        else:
            a = random.randint(0, random.randint(200, 250))
            b = random.randint(random.randint(20, 25), random.randint(25, 30))
            if a == b:
                cache.set(key="online-count-stockvip", value=count + 1, timeout=None)


# 更新数据库
class UpdateDB(Task):
    name = 'update-db'

    def run(self, *args, **kwargs):
        cache_count = cache.get("online-count-stockvip")
        try:
            db_count = OnlineMember.objects.get(id=1)
            if cache_count > db_count.people_count:
                db_count.people_count = cache_count
                db_count.save()
            else:
                count = random.randint(20, 50)
                cache.set(key="online-count-stockvip", value=db_count.people_count + count, timeout=None)
                db_count.people_count = db_count.people_count + count
                db_count.save()

        except:
            pass
