# -*- encoding: utf-8 -*-
'''
@File    :   test_api.py
@Time    :   2020/12/18 11:55:48
@Author  :   peace_su
@Version :   1.0
@Contact :   peace_su@163.com
@WebSite :   https://me.csdn.net/u010098760
'''

# here put the import lib
from logging import Logger
import pytest
import allure
import requests
from util import readXlsUtil, logUtil, glb
from util.baseApi import sendRequest, writeResult
from util.jsonPah import JsonPah
from util.replace import Replace
from util.copyXls import copyXls
from util.genSign import GenSign


# 用例路径
# caseXls = 'data\case1.xlsx'
# caseXls = 'data\\case1.xlsx'
caseXls = glb.xls_path
print(caseXls)
rxls = readXlsUtil.readXlsUtil(caseXls, 'Sheet1')
# 获取type为1的测试用例
caseData = rxls.dict_data(1)
# 获取用例名称
caseNames = rxls.dict_name(caseData)
# 测试结果文件
# reportXls = 'data\case1_report.xlsx'
# reportXls = 'data\\case1_report.xlsx'
reportXls = glb.xls_report_path
copyXls(caseXls, reportXls)


@allure.feature('测试某个功能')
class Test_api(object):

    def setup_class(self):
        self.logger = logUtil.Log('test_api').getlogger()
        self.tmp = {}
        self.session = requests.session()

    # @allure.story('查询企业信息')
    @pytest.mark.parametrize('data', caseData, ids=caseNames)
    def testApi(self, data):  # test method names begin with 'test'
        self.logger.info(
            '----用例[ %s ]------begin-------------' % data['caseId'])
        if self.tmp != {}:
            # 如果有关联参数，替换body、params、url、headers
            data['body'] = Replace(data['body'], self.tmp).replace()
            # 计算sign
            sign = GenSign('vtysJXstynJpIlEudO').genSign(data['body'])
            self.tmp['sign'] = sign
            data['params'] = Replace(data['params'], self.tmp).replace()
            data['url'] = Replace(data['url'], self.tmp).replace()
            data['headers'] = Replace(data['headers'], self.tmp).replace()
        # 发送请求
        result = sendRequest(self.session, data)
        # 如果存在re，就去响应中查找，找到后存到tmp中
        if data['re']:
            t = JsonPah(result['text'])
            param = t.jsonFind(data['re'])
            for j in param:
                self.tmp[j] = param[j]
        self.logger.info('保存的关联参数为：%s' % self.tmp)
        # 写结果
        writeResult(result, reportXls)
        # 开始断言
        assert result['result'] == 'pass'
        self.logger.info('----用例[ %s ]------end-------------' % data['caseId'])


if __name__ == '__main__':
    pytest.main(["--reruns", "1", "--reruns-delay",
                 "2", "--alluredir", "result"])
