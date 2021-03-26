from tasks.task_1 import *
from tasks.task_2 import *

if __name__ == '__main__':
    # res = test_1.delay(1, 2)
    # res = test_2_bind.delay(1, 2)
    # res = test_3_queue.delay(1, 2)
    # res = test_4_sub_task.delay(1, 2)
    res = test_5_base.delay(1, 2)
    print(res)

    # res = test_21.delay(1, 2)
    # res = test_22_bind.delay(1, 2)
    # res = test_23_queue.delay(1, 2)
    # print(res)

