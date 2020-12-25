# -*- encoding: utf-8 -*-
'''
@File    :   jsonPah.py
@Time    :   2020/12/18 15:34:19
@Author  :   peace_su
@Version :   1.0
@Contact :   peace_su@163.com
@WebSite :   https://me.csdn.net/u010098760
'''

# here put the import lib
import json
import execjs


class JsonPah(object):
    '''类注释
    详细描述

    Attributes:
        属性说明
    '''

    def __init__(self, o, mode='s'):
        self.json_object = None
        if mode == 'j':
            self.json_object = o
        elif mode == 's':
            self.json_object = json.loads(o)
        else:
            raise Exception('Unexpected mode argument.Choose "j" or "s".')

        self.result_list = []

    def jsonFind(self, keys):
        tmp = {}
        key_obj = json.loads(keys)
        for k in key_obj:
            tmp[k] = self.search_key(key_obj[k])

        return tmp

    def search_key(self, key):
        self.result_list = []
        real_key = key
        real_index = 0
        if '[' in key:
            real_key = key.split('[')[0]
            try:
                real_index = int(key.split('[')[1].split(']')[0])
            except:
                print('re字段错误，下标非int类型')
                return
        self.__search(self.json_object, real_key)
        if real_index < len(self.result_list) and real_index >= 0:
            return self.result_list[real_index]
        else:
            print('re字段错误，下标越界')
            return

    def __search(self, json_object, key):

        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self.__search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self.__search(item, key)
        return


if __name__ == '__main__':

    s1 = '{"return_code":"1000","return_message":"success","result_code":"0","result_message":"处理成功","access_token":123,"data":[{"access_token":"456","scope":"token","token_type":"bearer","expires_in":69272},{"access_token":"789","scope":"token","token_type":"bearer","expires_in":69272}]}'
    # s1 = '{"return_code":"1000","return_message":"success","result_code":"0","result_message":"处理成功","access_token":123,"data":{"access_token":"afdb9572-4993-4af4-9395-476c7646f398","scope":"token","token_type":"bearer","expires_in":69272}}'
    j1 = '{"token":"access_token[2]","time":"expires_in"}'
    t = JsonPah(s1)
    # print(t.search_key('access_token[2]'))

    print(t.jsonFind(j1))

    xxx = execjs.compile('''
        function add(){
      var a=100;
      var b=10;
      return a+b;
    }
    ''')
    print(xxx.call("add"))
