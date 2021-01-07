# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/10/12 21:49
# file:glb.py
# desc: 定义全局变量
import os
import time

reportPath_base = os.path.abspath(os.path.join(os.getcwd(), 'report'))
# 判断是否有report目录，没有就创建
if not os.path.exists(reportPath_base):
    os.mkdir(reportPath_base)

ctime = time.strftime('%Y%m%d', time.localtime(time.time()))
reportPath = os.path.join(reportPath_base, ctime)
# 判断report下边是否有时间戳文件夹，没有就新建
if not os.path.exists(reportPath):
    os.mkdir(reportPath)

if not os.path.exists('log'):
    os.mkdir('log')
logPath = os.path.join('log', ctime)

dataPath = os.path.abspath(os.path.join(os.getcwd(), 'data'))

# 要执行的用例文件路径，eg: data\case1.xlsx
xls_path = ''
# 要保持的结果文件的路径，eg: data\case1_report.xls
xls_report_path = ''
