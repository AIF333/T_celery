from kombu import Queue


celery_conf = {
    'broker_url': 'redis://:123456@192.168.99.100:6399/2',
    'result_backend': 'redis://:123456@192.168.99.100:6399/3',
    'CELERY_TRANSPORT': 'redis',
    'redis_max_connections': 4,
    'worker_concurrency': 4,  # 并发数
    'broker_transport_options': {'visibility_timeout': 43200,  # 43200min
                                 'max_connections': 128},
    'result_expires': 3600,  # 任务结果保存时间
    'broker_pool_limit': 128,  # broker连接池，默认10
    'task_acks_late': True,  # 只有当worker完成了这个task时，任务才被标记为ack状态
    'task_reject_on_worker_lost': True,  # 当worker进程意外退出时，task会被放回到队列中，可能重复执行
    # 'CELERYD_FORCE_EXECV': True,  # 非常重要,有些情况下可以防止死锁， 5.0已被删除
    'worker_max_memory_per_child': 10,  # 每个worker最多执行100个任务就会被销毁，可防止内存泄露

    'task_ignore_result': True,  # 不保存任务结果

    'task_serializer': 'pickle',
    'result_serializer': 'json',
    'accept_content': ['pickle', 'json'],  # Ignore other content
    'enable_utc': False,
    'timezone': 'Asia/Shanghai',
    'worker_prefetch_multiplier': 1,  # worker预取任务数，保证任务优先级生效
}

include = [
    'tasks.task_1',
    # 'tasks.task_2',
]

task_conf = {

    'task_queues': (  # 创建任务队列
        Queue('default', routing_key='task.#'),  # 默认任务队列
        Queue('user_quick', routing_key='user_quick.#'),  # 用户快速任务 < 10s
        Queue('user_normal', routing_key='user_normal.#'),  # 用户一般任务 10-300s
        Queue('user_large', routing_key='user_large.#'),  # 用户大任务 > 300s
        Queue('inner_quick', routing_key='inner_quick.#'),  # 内部快速任务 < 10s
        Queue('inner_normal', routing_key='inner_normal.#'),  # 内部一般任务 10-300s
        Queue('inner_large', routing_key='inner_large.#'),  # 内部大任务 > 300s
    ),
    # 默认任务队列
    'task_default_queue': 'default',
    'task_default_exchange': 'task',
    'task_default_exchange_type': 'topic',
    'task_default_routing_key': 'task.default',

    'task_routes': {  # 指定任务的任务队列， 这里配置了则文件下方法用装饰器调整是无效的
        # 用户快速任务
        'tasks.task_1.*': {
            'queue': 'user_quick',  # 队列名称
            'routing_key': 'user_quick.task',  # key 匹配 task_queues中的 .# , user_quick.aaa也可以
            'priority': 0,  # 任务优先度，支持同队列，跨队列，redis：0是最高优先级; 内部方法的优先级会替换这里的(与queue不同)
        }
    }
}
