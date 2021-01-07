from logging import raiseExceptions
import logging
from util.logUtil import Log

logger = Log('deco').getlogger()


# 判断method是否合法装饰器
def decoJudgeMethod(func):
    def wrapper(*args, **kwargs):
        testData = args[1]
        ret = None
        if testData['method'].upper() == 'POST' or testData['method'].upper() == 'GET':
            ret = func(*args, **kwargs)
        else:
            logger.error('method必须为post或者get，传入值为%s，请检查！' % testData['method'])
            raise ValueError('method必须为post或者get，传入值为%s，请检查！' %
                             testData['method'])
        return ret
    return wrapper
