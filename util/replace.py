# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/10/20 21:43
# file:replace
# desc: 替换请求参数中的变量

import re
from util.regFindString import regFindString
import json


class Replace:
    def __init__(self, old, param):
        self.old = old
        self.param = param

    def replace(self):
        l = re.findall(r"\${(.+?)}", self.old)

        for i in l:
            self.old = self.old.replace("${" + i + "}", self.param[i])

        return self.old


if __name__ == "__main__":
    body = '{"tableKey":"${tablekey}","soupOrder":"Y","orderKey":"${orderKey}"}'
    s1 = "var tableKey = '201810207131C9157F2D4FE3A59C111'; // 桌台码  " \
        "var orderKey = '7131C9157F2D4FE3A59C_o29U5wq7XF-OutcJRojtmO2exjhY_orders';"
    js = "{\"tablekey\":\"tableKey = '(.+?)';\",\"orderKey\":\"orderKey = '(.+?)';\"}"

    # print(type(body))
    # body = json.loads(body)
    # print(type(body))

    p = regFindString(s1, js).find()
    print(p)
    n = Replace(body, p).replace()
    print(n)

    tmp = {}
    if tmp == {}:
        print(1111)
    else:
        print(222)
