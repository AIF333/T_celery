import time
import datetime
from hdy_celery.hdy_celery import app
from tasks.task_base import MyTask111
from .task_2 import test_21


@app.task()
def test_1(a, b):
    """基础调用"""
    print("test_1 start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(1)
    print("test_1 end :%s" % datetime.datetime.now())
    return {'test_1': 1}


@app.task(bind=True, priority=6)
def test_2_bind(self, a, b):
    """绑定任务，设置优先级，绑定后第一个参数是self"""
    # eg: task=' tasks.task_1.test_2_bind', id='cc44ed59-6c03-4440-947c-671747b7d799', routing_key='user_quick.task'
    # delivery_info: {'exchange': 'task', 'routing_key': 'user_quick.task', 'priority': 0, 'redelivered': None}
    try:
        print(self.request.task, self.request.id, self.request.delivery_info, self.request)
        print("test_2_bind start :%s" % datetime.datetime.now())
        print('a=%s, b=%s' % (a, b))
        time.sleep(2)
        print("test_2_bind end :%s" % datetime.datetime.now())
        # c = 1 / 0
        return {'test_2_bind': 1}
    except Exception as e:
        print(e)
        # 当任务失败则进行重试，也可以通过max_retries属性来指定最大重试次数, 默认3次
        # countdown 多长时间重试，默认是 180s
        self.retry(max_retries=1, countdown=10)


@app.task(queue='user_large')
def test_3_queue(a, b):
    """调用子任务、设置队列，如果在settings中对整个文件有设置，那么这里的设置将不生效"""
    print("test_3_queue start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(2)
    test_21.delay(a, b)
    print("test_3_queue end :%s" % datetime.datetime.now())
    return {'test_3_queue': 1}


@app.task(queue='user_large', priority=9)
def test_4_sub_task(a, b):
    """调用子任务"""
    print("test_4_sub_task start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    test_3_queue.delay(a, b)
    time.sleep(2)
    print("test_4_sub_task end :%s" % datetime.datetime.now())
    return {'test_4_sub_task': 1}


@app.task(base=MyTask111)
def test_5_base(a, b):
    """测试自定义base基类"""
    print("test_5_base start :%s" % datetime.datetime.now())
    print('a=%s, b=%s' % (a, b))
    time.sleep(2)
    print("test_5_base end :%s" % datetime.datetime.now())
    raise Exception('this is a exception')
    return {'test_5_base': 1}


