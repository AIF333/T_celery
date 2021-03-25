import datetime
import time
from celery import Celery
import celeryconfig

app = Celery()
app.config_from_object(celeryconfig.CELERY)


@app.task
def test_1(a, b):
    print("test_1 start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(1)
    print("test_1 end :%s" % datetime.datetime.now())


# celery -A tasks worker --loglevel=info  -P eventlet
