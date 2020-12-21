# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/10/12 9:36
# file:loadConf
# desc: 读取配置文件

import configparser
import os

# 配置文件路径
confPath = os.path.abspath(os.path.join(os.getcwd(), "conf"))
confFile = os.path.join(confPath, 'config.conf')
cf = configparser.ConfigParser()
cf.read(confFile, encoding='utf8')


class loadConf():

    @classmethod
    def get_config(cls, section, option):
        value = ''
        try:
            value = cf.get(section, option)
        except:
            print('section、option填写有误，请检查')
        finally:
            return value


if __name__ == '__main__':
    x = loadConf.get_config('test_api', 'report_file')
    print(type(x))
    y = loadConf.get_config('test_process', 'data_file')
    print(y)
    # path = os.path.join(confPath,x)
    # print(path)
