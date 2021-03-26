import datetime
import time


def get_timestamp():
    return int(time.time() * 1000)


def now_yyyymmddhhmmss():
    '''
    @return: 当天时间 如 2018-12-12 20:57:43
    '''
    dtstr = str(datetime.datetime.now())
    return dtstr.split('.')[0]