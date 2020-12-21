# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/9/30 10:48
# file:baseApi
# desc: 封装http请求，写测试结果

import json
import requests
from util.copyXls import writeXls, copyXls
from util.readXlsUtil import readXlsUtil
from util.logUtil import Log

logger = Log('baseApi').getlogger()


def sendRequest(session, testData):
    '''封装requests请求'''
    # print('testdata:%s'%testData)
    caseId = testData['caseId']
    method = testData['method']
    url = testData['url']
    try:
        params = eval(testData['params'])
    except:
        params = None
        logger.info('请求params 为空')

    try:
        headers = eval(testData['headers'])
    except:
        headers = None
        logger.info('请求headers 为空')
    bodyType = testData['bodyType']

    logger.info("*******正在执行用例：-----  %s  ----**********" % caseId)
    logger.info("请求方式：%s, 请求url:%s" % (method, url))
    logger.info("请求params：%s" % params)
    logger.info("请求headers：%s" % headers)

    try:
        body = eval(testData['body'])
    except:
        body = {}
        logger.info('请求dody 为空')

    if bodyType == 'json':
        body = json.dumps(body)
    else:
        logger.info('请求body_type 为空')
        body = body
    if method == 'post':
        logger.info("post请求body类型为：%s，body内容为：%s" % (bodyType, body))

    verify = False
    result = {}

    try:
        response = session.request(method=method,
                                   url=url,
                                   params=params,
                                   headers=headers,
                                   data=body,
                                   verify=verify
                                   )

        logger.info("返回信息：%s" % response.content.decode('utf-8'))
        if 'sheetName' in testData.keys():
            result['sheetName'] = testData['sheetName']
        else:
            result['sheetName'] = 'Sheet1'

        result['id'] = testData['caseId']
        result['rowNum'] = testData['rowNum']
        result["statusCode"] = str(response.status_code)  # 状态码转成str
        result["text"] = response.content.decode("utf-8")
        result["times"] = str(response.elapsed.total_seconds())  # 接口请求时间转str
        # 判断http状态码，如果不是200，判定为失败
        if result["statusCode"] != "200":
            result["error"] = result["text"]
            result["result"] = "fail"
        else:   # 如果http状态码是200，进行检查点的判断
            result["error"] = ""
            if testData["checkpoint"] in result["text"]:
                result["result"] = "pass"
            else:
                result["result"] = "fail"
        # return result
    except Exception as e:
        result['error'] = str(e)
        result['result'] = 'fail'
        logger.error('请求报错，错误信息为：%s' % str(e))
        # return result
    finally:
        logger.info("用例测试结果:   %s---->%s" % (caseId, result["result"]))
        # print("result:%s" % result)
        return result


def writeResult(result, filename):
    rowNum = result['rowNum']
    wt = writeXls(filename)
    wt.write(rowNum, 9, result['statusCode'])
    wt.write(rowNum, 10, result['text'])
    wt.write(rowNum, 11, result['error'])
    wt.write(rowNum, 12, result['times'])
    wt.write(rowNum, 13, result['result'])


def writeResult2(result, filename):
    wt = writeXls(filename)
    wt.write2(result['sheetName'], result['rowNum'], 9, result['statusCode'])
    wt.write2(result['sheetName'], result['rowNum'], 10, result['text'])
    wt.write2(result['sheetName'], result['rowNum'], 11, result['error'])
    wt.write2(result['sheetName'], result['rowNum'], 12, result['times'])
    wt.write2(result['sheetName'], result['rowNum'], 13, result['result'])


if __name__ == '__main__':
    testData = readXlsUtil('../data/case1.xlsx', 'sheet1').dict_data(1)
    session = requests.session()
    result = sendRequest(session, testData[0])
    copyXls('../data/case1.xlsx', '../report/case1_result.xlsx')
    writeResult(result, '../report/case1_result.xlsx')
