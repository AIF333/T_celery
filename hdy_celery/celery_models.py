from mongoengine import Document, fields, connect

from utils import get_timestamp, now_yyyymmddhhmmss


class ControlTypeEnum:
    queue = 'queue'
    func = 'func'


class ControlValidEnum:
    invalid = 0  # 无效
    valid = 1  # 有效


class ControlRmCurrentEnum:
    no = 'no'  # 不删除
    read2rm = 'read2rm'  # 准备删除
    already = 'already'  # 已删除


connect(db='yt_test', host='192.168.99.100', port=53015, username='yeteng', password='123456')


class CeleryTaskControl(Document):
    """celery的控制模型"""
    queue = fields.StringField(verbose_name='任务队列名, eg: inner_quick', require=True)
    control_type = fields.StringField(verbose_name='控制类别', require=True, default=ControlTypeEnum.func)
    func = fields.StringField(verbose_name='方法名: test_1, 当控制类别为func时必填')
    start_time = fields.LongField(verbose_name='开始生效时间', default=get_timestamp)
    end_time = fields.LongField(verbose_name='结束生效时间', default=0)
    rm_current_tasks = fields.StringField(verbose_name='删除现有未执行的任务，当控制类别为queue时有效', default=ControlRmCurrentEnum.no)
    status = fields.IntField(verbose_name='启用状态', require=True, default=ControlValidEnum.valid)

    meta = {'collection': 'hdy_celery_control', 'indexes': ['start_time', 'end_time', 'status']}


class CeleryErrorRecord(Document):
    """celery执行的错误记录"""
    task_id = fields.StringField(verbose_name='celery任务id', require=True, primary_key=True)
    full_func = fields.StringField(verbose_name='带路径的方法名，eg: tasks.task_1.test_1')
    func_params = fields.DictField(verbose_name='方法参数 {args:(), kwargs: {}}')
    exc = fields.StringField(verbose_name='简短异常说明')
    error_info = fields.StringField(verbose_name='异常堆栈详细信息')
    create_time = fields.LongField(verbose_name='创建时间', default=get_timestamp)
    create_time_human = fields.StringField(verbose_name='创建时间,人看的', default=now_yyyymmddhhmmss)

    meta = {'collection': 'hdy_celery_error', 'indexes': ['full_func', 'create_time', 'create_time_human']}


if __name__ == '__main__':
    a = CeleryTaskControl()
    a.queue = 'inner_quick'
    a.func = 'test_1'
    a.save()
