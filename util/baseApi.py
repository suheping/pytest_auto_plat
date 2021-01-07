# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/9/30 10:48
# file:baseApi
# desc: 封装http请求，写测试结果

from email import header
import json
import os
import requests
from util.copyXls import writeXls, copyXls
from util.readXlsUtil import readXlsUtil
from util.logUtil import Log
from util import deco

logger = Log('baseApi').getlogger()


@deco.decoJudgeMethod
def sendRequest(session, testData):
    '''封装requests请求'''
    # print('testdata:%s'%testData)

    caseId = testData['caseId']
    method = testData['method']
    url = testData['url']
    bodyType = testData['bodyType']
    body = testData['body']
    # 判断bodyType，格式化body
    if bodyType == 'json':
        if body == '':
            body = {}
        else:
            try:
                body = eval(testData['body'])
                body = json.dumps(body)
            except:
                body = {}
                logger.info('body格式化为json失败，请检查')
    elif bodyType == 'file':
        body = testData['body']
    else:
        logger.info('请求body_type为其他格式，请填写json或file')

    # 格式化params
    try:
        params = eval(testData['params'])
    except:
        params = None
        logger.info('params格式化为json失败，请检查')

    # 格式化headers
    try:
        headers = eval(testData['headers'])
    except:
        headers = None
        logger.info('headers格式化为json失败，请检查')

    verify = False
    result = {}

    logger.info("请求方式：%s, 请求url:%s" % (method, url))
    logger.info("请求params：%s" % params)
    logger.info("请求headers：%s" % headers)
    logger.info('请求body：%s' % body)
    try:
        response = None
        if bodyType == 'json':
            response = session.request(method=method,
                                       url=url,
                                       params=params,
                                       headers=headers,
                                       data=body,
                                       verify=verify
                                       )
        elif bodyType == 'file':
            uploadFile = {'file': open(body, 'rb')}
            response = session.request(method=method,
                                       url=url,
                                       params=params,
                                       headers=headers,
                                       files=uploadFile,
                                       verify=verify
                                       )
        responseType = response.headers['Content-Type']
        # 判断响应的数据类型
        if responseType == 'application/json':
            logger.info("返回信息：%s" % response.content.decode('utf-8'))
            result["text"] = response.content.decode("utf-8")
        elif responseType == 'application/octet-stream; charset=utf-8':
            logger.info('返回为字节流，大小为%sB' % response.headers['Content-Length'])
            result["text"] = '字节流，大小为%sB' % response.headers['Content-Length']
            result["result"] = "pass"
            result['error'] = ""
            # 将字节流保存到本地
            downloadPath = 'data\\download\\'
            if not os.path.exists(downloadPath):
                os.mkdir(downloadPath)
            savedFile = downloadPath + \
                response.headers['Content-Disposition'].split('=')[1]
            with open(savedFile, "wb") as code:
                code.write(response.content)
        else:
            # 待判断
            pass
        if 'sheetName' in testData.keys():
            result['sheetName'] = testData['sheetName']
        else:
            result['sheetName'] = 'Sheet1'

        result['id'] = testData['caseId']
        result['rowNum'] = testData['rowNum']
        result["statusCode"] = str(response.status_code)  # 状态码转成str
        result["times"] = str(response.elapsed.total_seconds())  # 接口请求时间转str

        # 判断http状态码，如果不是200，判定为失败
        if result["statusCode"] != "200":
            result["error"] = result["text"]
            result["result"] = "fail"
        else:   # 如果http状态码是200，进行检查点的判断
            if responseType == 'application/json':
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
        logger.info("用例%s测试结果[ %s ]" % (caseId, result["result"]))
        # print("result:%s" % result)
        return result


def writeResult(result, filename):
    rowNum = result['rowNum']
    wt = writeXls(filename)
    wt.write(rowNum, 10, result['statusCode'])
    wt.write(rowNum, 11, result['text'])
    wt.write(rowNum, 12, result['error'])
    wt.write(rowNum, 13, result['times'])
    wt.write(rowNum, 14, result['result'])


def writeResult2(result, filename):
    wt = writeXls(filename)
    wt.write2(result['sheetName'], result['rowNum'], 9, result['statusCode'])
    wt.write2(result['sheetName'], result['rowNum'], 10, result['text'])
    wt.write2(result['sheetName'], result['rowNum'], 11, result['error'])
    wt.write2(result['sheetName'], result['rowNum'], 12, result['times'])
    wt.write2(result['sheetName'], result['rowNum'], 13, result['result'])


if __name__ == '__main__':
    # testData = readXlsUtil('../data/case1.xlsx', 'sheet1').dict_data(1)
    # session = requests.session()
    # result = sendRequest(session, testData[0])
    # copyXls('../data/case1.xlsx', '../report/case1_result.xlsx')
    # writeResult(result, '../report/case1_result.xlsx')

    # 文件上传测试
    # file = {'file': open(
    #     'data\\files\\公章.png', 'rb')}
    # session = requests.session()
    # response = session.request(url='http://192.168.1.206:9000/api/v1/file/upload', method='post', params={"file_type": "impression", "file_name": "测试公章", "user_id": "00788730734155812864"}, headers={
    #                            "token": "0a5946bf-ae2c-4063-97a8-41d1fadf939d"}, files=file)
    # print(response.text)
    pass
