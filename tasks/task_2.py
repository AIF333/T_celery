import time
import datetime
from hdy_celery.hdy_celery import app


@app.task(queue='inner_quick')
def test_21(a, b):
    print("test_21 start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(1)
    # 测试子任务
    test_22_bind.delay(3, 4)
    print("test_21 end :%s" % datetime.datetime.now())
    return {'test_21': 1}


@app.task(bind=True, queue='inner_normal')
def test_22_bind(self, a, b):
    # eg: task=' tasks.task_1.test_2_bind', id='cc44ed59-6c03-4440-947c-671747b7d799', routing_key='user_quick.task'
    # delivery_info: {'exchange': 'task', 'routing_key': 'user_quick.task', 'priority': 0, 'redelivered': None}
    try:
        print(self.request.task, self.request.id, self.request.delivery_info, self.request)
        print("test_22_bind start :%s" % datetime.datetime.now())
        print('a=%s, b=%s' % (a, b))
        time.sleep(2)
        print("test_22_bind end :%s" % datetime.datetime.now())
        c = 1 / 0
        return {'test_22_bind': 1}
    except Exception as e:
        print(e)
        # 当任务失败则进行重试，也可以通过max_retries属性来指定最大重试次数, 默认3次
        # countdown 多长时间重试，默认是 180s
        # args 和 kwargs 默认用原参数的，可不传
        self.retry(max_retries=5, countdown=5)


@app.task(queue='inner_large')
def test_23_queue(a, b):
    print("test_23_queue start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(2)
    print("test_23_queue end :%s" % datetime.datetime.now())
    return {'test_23_queue': 1}

# celery -A tasks worker --loglevel=info  -P eventlet
