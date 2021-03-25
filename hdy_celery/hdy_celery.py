from __future__ import absolute_import

from celery import Celery, platforms, shared_task
from hdy_celery.celeryconfig import include, task_conf, celery_conf


platforms.C_FORCE_ROOT = True  # 解决root账户下不能启动celery的问题

app = Celery(include=include)
app.config_from_object(celery_conf)
app.conf.update(task_conf)

shared_task = shared_task
