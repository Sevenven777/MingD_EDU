# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 8:20 PM'

from random import Random
from django.core.mail import send_mail
from users.models import *
from myonline.settings import EMAIL_FROM


def send_register_emall(email, send_type=1):
    email_record = EmailVerifyCode()
    code = generate_random_str(4)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    if send_type == 1:
        email_title = "铭德教育在线课堂注册激活链接"
        email_body = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False

    if send_type == 2:
        email_title = "铭德教育在线课堂密码重置链接"
        email_body = "请点击下面的链接重置您的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False

    if send_type == 3:
        email_title = "铭德教育在线课堂邮箱重置链接"
        email_body = '用户邮箱修改确认验证码：{} （区分大小写）'.format(code)


        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False

def generate_random_str(randomlength=8):
    mystr = ""
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        mystr += chars[random.randint(0, length)]
    return mystr
