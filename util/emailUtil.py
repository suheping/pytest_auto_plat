# -*- coding:utf-8 -*-
# author:peace
# datetime:2018/10/12 20:26
# file:emailUtil
# desc: 发送邮件工具类

# 导入smtplib模块
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from util.loadConf import loadConf


def send_email(subject, content):
    # 配置文件中配置的数据
    SMTP_host = loadConf.get_config('email', 'SMTP_host')
    from_addr = loadConf.get_config('email', 'from_addr')
    password = loadConf.get_config('email', 'password')
    to_addrs_list = loadConf.get_config('email', 'to_addrs').split(',')
    #
    email_client = SMTP(SMTP_host)
    email_client.login(from_addr, password)
    # 发送纯文本邮件 设置为plain,发送html邮件修改为 MIMEText(content,'html','utf-8')
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addrs_list)
    # sendmail(邮件发送者地址，字符串列表（收件人），发送内容)
    # 发送纯文本邮件
    email_client.sendmail(from_addr, to_addrs_list, msg.as_string())


if __name__ == '__main__':

    subject = '邮件标题'
    content = '邮件正文'

    send_email(subject, content)
