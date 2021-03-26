import collections
import copy

from celery import Celery, Task, platforms

from hdy_celery.celery_models import CeleryTaskControl, ControlTypeEnum, ControlValidEnum, CeleryErrorRecord
from utils import get_timestamp

platforms.C_FORCE_ROOT = True


class Mycelery(Celery):
    def task(self, *args, **opts):
        """指定celery的基类，这个是在项目启动时调用"""
        # 指定了base必须继承MyTask
        base = opts.get('base', BaseTask)
        if not issubclass(base, BaseTask):
            raise Exception("base=%s is not BaseTask's subclass" % base)
        opts['base'] = base

        # 不允许用修改任务名称，强制使用默认 eg: 'tasks.task_1.test_3_queue'， 后面的统一处理和动态干预都依赖这个名称
        if 'name' in opts:
            # 启动worker时也会调用这里，类似于 name=celery.chord_unlock ，这里放开
            if not opts['name'].startswith('celery.'):
                raise Exception("name=%s is not support in Mycelery" % opts['name'])
        return super(Mycelery, self).task(*args, **opts)

    def send_task(self, name, args=None, kwargs=None, countdown=None,
                  eta=None, task_id=None, producer=None, connection=None,
                  router=None, result_cls=None, expires=None,
                  publisher=None, link=None, link_error=None,
                  add_to_parent=True, group_id=None, group_index=None,
                  retries=0, chord=None,
                  reply_to=None, time_limit=None, soft_time_limit=None,
                  root_id=None, parent_id=None, route_name=None,
                  shadow=None, chain=None, task_type=None, **options):
        """
        通过name发送消息，这里做特殊处理：
        可以检验消息的队列和方法名，当数据库设置为暂停时，则不再发送消息。如资源紧张时将内部的任务临时暂停
        """
        run_flag, queue_name = CheckTask.check_before_create(name, args, kwargs, router, task_type,
                                                             route_name, self.amqp, **options)

        if run_flag:
            return super(Mycelery, self).send_task(name, args, kwargs, countdown,
                                                   eta, task_id, producer, connection,
                                                   router, result_cls, expires,
                                                   publisher, link, link_error,
                                                   add_to_parent, group_id, group_index,
                                                   retries, chord,
                                                   reply_to, time_limit, soft_time_limit,
                                                   root_id, parent_id, route_name,
                                                   shadow, chain, task_type, **options)
        else:
            print('queue=%s, func=%s, is stop in config, pass' % (queue_name, name))


class BaseTask(Task):
    """
    好队友的任务处理后的钩子基类， 这里定义通用方法，子类可以自定义继承
    说明： after_return 这个不需要，相当于 on_failure/on_success 的后手，且当 on_failure/on_success有内部错误时是无法进入的
    """

    # 任务执行
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        任务失败时，记录错误日志
        :param exc: 错误简短描述，是对象，str(exc)
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo: 错误异常堆栈，，是对象str(einfo)
        常用: self，name 方法全名，eg: tasks.task_1.test_1
        """
        try:
            print('on_failure: --------%s' % self.name)
            err_obj = CeleryErrorRecord.objects.filter(task_id=task_id).first()
            err_obj = err_obj or CeleryErrorRecord()
            err_obj.task_id = task_id
            err_obj.full_func = self.name
            err_obj.func_params = {'args': args, 'kwargs': kwargs}
            err_obj.exc = str(exc)
            err_obj.error_info = str(einfo)
            err_obj.save()
        except Exception as e:
            # TODO yeteng 20210326 发送钉钉通知？
            print(e)

    def on_success(self, retval, task_id, args, kwargs):
        """
        任务成功时, 实现依赖任务用这个，A执行完才能执行B， 则将B的生成写在A的这里
        :param retval: 方法返回值
        :param task_id:
        :param args:
        :param kwargs:
        常用: self，name 方法全名，eg: tasks.task_1.test_1
        """
        print('on_success: --------%s' % self.request.task)
        # print('self=%s， self__dict__=%s, self.request.task=%s, self.request=%s' % (self, self.__dict__, self.request.task, self.request))
        # print('retval=%s' % retval)
        # print('task_id=%s' % task_id)
        # print('args= ', args)
        # print('kwargs=%s' % kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        任务重试时
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo: 错误异常堆栈
        常用: self，name 方法全名，eg: tasks.task_1.test_1
        """
        print('on_retry: --------%s' % self.request.task)
        # print('self=%s， self__dict__=%s, self.request.task=%s, self.request=%s' % (self, self.__dict__, self.request.task, self.request))
        # print('exc=%s' % exc)
        # print('task_id=%s' % task_id)
        # print('args= ', args)
        # print('kwargs=%s' % kwargs)
        # print('einfo=%s' % einfo)


class CheckTask(object):
    """celery任务的处理类，提供处理方法"""

    @staticmethod
    def check_before_create(name, args, kwargs, router, task_type, route_name, amqp, **options):
        """创建任务前的检查处理"""
        # TODO yeteng 20210325 这里需要设置1个缓存，配置表的有效暂停数据
        #  rm_current_tasks逻辑未加上
        run_flag = True
        # 深拷贝，免得影响后续业务
        c_options = copy.deepcopy(options)
        c_route_name = route_name
        c_name = name
        c_args = copy.deepcopy(args)
        c_kwargs = copy.deepcopy(kwargs)

        c_router = router or amqp.router
        c_options.pop('ignore_result', False)
        c_options = c_router.route(
            c_options, c_route_name or c_name, c_args, c_kwargs, task_type)

        # 校验逻辑
        queue = c_options.get('queue')
        queue_name = None
        if queue:
            queue_name = queue.name
            print(queue_name, name)
            now_time = get_timestamp()
            # 校验queue，筛选有效的需要暂停的queue
            control_objs = CeleryTaskControl.objects.filter(
                start_time__lte=now_time,
                end_time__gte=now_time,
                status=ControlValidEnum.valid
            )
            stop_queues = []
            stop_func_dict = collections.defaultdict(list)  # {queue: [func_1, func_2]}
            for obj in control_objs:
                if obj.control_type == ControlTypeEnum.queue:
                    stop_queues.append(obj.queue)
                elif obj.control_type == ControlTypeEnum.func:
                    stop_func_dict[obj.queue].append(obj.func)

            stop_funcs = stop_func_dict.get(queue_name)

            # c_name eg: 'tasks.task_1.test_1'
            func = c_name.split('.')[-1]
            if (queue_name in stop_queues) or (stop_funcs and func in stop_funcs):
                run_flag = False

        return run_flag, queue_name



