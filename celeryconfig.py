CELERY = {
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