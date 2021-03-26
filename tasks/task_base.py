from hdy_celery.my_celery import BaseTask


class MyTask111(BaseTask):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("AIF333------------------ on_failure, %s" % self.name)
        super(MyTask111, self).on_failure(exc, task_id, args, kwargs, einfo)
        print("AIF333------------------ on_failure end, %s" % self.name)

    def on_success(self, retval, task_id, args, kwargs):
        print("AIF333------------------ on_success, %s" % self.name)
        super(MyTask111, self).on_success( retval, task_id, args, kwargs)
        print("AIF333------------------ on_success end, %s" % self.name)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print("AIF333------------------ on_retry, %s" % self.name)

