# 1 设计思路

1. 通过`requests`发送 http 请求
2. 通过`pytest`实现单元测试
3. 通过`@pytest.mark.parametrize`实现数据驱动
4. 通过`allure`实现测试报告展示
5. 通过`logging`实现日志记录
6. 通过`excel`编写测试用例
7. 实现用例间`关联`功能
8. 前置、后置脚本功能（js）---待实现

# 2 框架介绍

1. 入口文件[run.py](/run.py)
2. excel 用例文件[case1.xlsx](/data/case1.xlsx)
3. 待上传文件存放路径[files](/data/files)
4. 下载文件存放路径[download](/data/download)
5. 日志路径`/log`
6. 生成的测试结果文件[case1_report.xlsx](/data/case1_report.xlsx)
7. 生成的 allure 结果路径`/result`
8. 生成的 allure 报告路径`/report`
9. 接口测试类文件路径[test_api.py](/testcase/test_api.py)
10. http 请求工具类路径[baseApi.py](/util/baseApi.py)
11. 关联工具类路径[jsonPath.py](/util/jsonPath.py) [replace.py](/util/replace.py)
12. 日志工具类路径[logUtil.py](/util/logUtil.py)

# 3 使用说明

1. 安装依赖，在项目根目录下执行`pip install -r require.txt`
2. 修改/data/case1.xlsx 用例文件
3. 执行 run.py`python run.py`
4. 生成报告`allure generate result -o report --clean`
5. 查看报告，用 vscode 的 live server 打开/report/index.html

# 4 jenkins 持续集成

1. jenkins 中配置源码 git 路径
2. jenkins 中配置 allure
3. 构建，查看报告

# 5 联系我

![peace测试空间](/data/files/qrcode.jpg '扫码关注我')
