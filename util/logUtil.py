# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/10/12 18:01
# file:mylog
# desc: 日志工具类

import logging
import os
from util import glb

logPath = glb.logPath

if not os.path.exists(logPath):
    os.mkdir(logPath)
logfile = os.path.join(logPath, 'output.log')


class Log(object):

    def __init__(self, name):
        self.logfile = logfile
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        # 输出日志到文件
        handler = logging.FileHandler(self.logfile, encoding='utf-8')
        self.fh = handler
        self.fh.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(threadName)s - %(name)s[%(lineno)s] - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        # 关闭打开的文件
        self.fh.close()

    def getlogger(self):
        return self.logger


if __name__ == '__main__':
    logger = Log('testlog').getlogger()
    logger.info('suheping')
