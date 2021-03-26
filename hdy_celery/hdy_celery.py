from __future__ import absolute_import

from hdy_celery.celeryconfig import include, task_conf, celery_conf
from hdy_celery.my_celery import Mycelery, platforms

platforms.C_FORCE_ROOT = True  # 解决root账户下不能启动celery的问题

app = Mycelery(include=include)
app.config_from_object(celery_conf)
app.conf.update(task_conf)
