##### 说明：        

* 通过继承和调整部分方法，使celery支持动态暂停和恢复任务
* 增加统一的任务完成后的钩子类BaseTask

##### 实现原理：

* 复用celery的send_task方法，满足校验规则的才进行消息发送

##### 局限：   

* 基于 celery==5.0.2 版本



##### 代码说明：
* hdy_celery
  * celery_models.py   celery的控制和日志记录模型
  * celeryconfig.py   celery的启动配置文件
  * my_celery.py   为对源码的继承和修改
  * hdy_celery.py   给外部导包使用的Mycelery对象
* tasks 
  * task_1.py  测试任务脚本1
  * task_2.py 测试任务脚本2
  * task_base.py  自定义的base
* utils 工具类