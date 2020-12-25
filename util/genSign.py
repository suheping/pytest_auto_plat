# -*- encoding: utf-8 -*-
'''
@File    :   genSign.py
@Time    :   2020/12/22 10:08:50
@Author  :   peace_su
@Version :   1.0
@Contact :   peace_su@163.com
@WebSite :   https://me.csdn.net/u010098760
'''

# here put the import lib
import hashlib
import hmac
import base64
import chardet
from util.logUtil import Log

logger = Log('genSign').getlogger()


class GenSign(object):
    '''类注释
    详细描述

    Attributes:
        属性说明
    '''

    def __init__(self, key):
        '''类初始化方法

        Args:
            paramter1: 入参说明
            paramter2: 入参说明
        '''

        self.key = key

    def genSign(self, body):
        '''方法注释
        方法描述

        Args:
        paramter1: 入参说明
        paramter2: 入参说明

        Returns:
            返回描述

        Raises:
            抛出异常说明
        '''
        logger.info('计算sign的body为：%s' % body)
        key = self.key.encode('utf-8')
        body = body.replace(' ', '').replace(
            '\n', '').replace('\r', '').replace('\v', '').replace('\t', '').replace('\f', '').encode('utf-8')

        s256 = hmac.new(key, body, digestmod=hashlib.sha256).digest()
        b64 = base64.b64encode(s256)
        res = hashlib.md5(b64).hexdigest().upper()

        return res


if __name__ == '__main__':
    body = '{"file_id": "f1ddf9f837781ca3bfaa3e06ecaf244d", "seal_name": "test-gongzhang", "seal_type": "01", "size": "40*40", "user_id": "10788733057439518720", "description": "exercitationesseinnonipsum"}'
    key = 'vtysJXstynJpIlEudO'
    t = GenSign(key)
    print(t.genSign(body))
    # C1A2D06078E8CC9219559A85830C0A36
    # x = hmac.new(key.encode('utf-8'),
    #              body.replace(" ", "").encode(
    #                  'utf-8'),
    #              digestmod=hashlib.sha256).digest()

    # y = base64.b64encode(x)
    # z = hashlib.md5(y).hexdigest()
    # # print(chardet.detect(z))
    # print(str(z).upper())
