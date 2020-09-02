# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/21/2020 9:20 PM'

from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # 用户信息
    path(r'info/', UserinfoView.as_view(), name="user_info"),
    # 用户头像上传
    path(r'image/upload/', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修改密码
    path(r'update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    # 用户个人中心修改信息
    path(r'update/info/', UserInfoChangeView.as_view(), name="update_info"),
    # 用户修改邮箱发送验证码
    path('verify_code/send/', ModifyEmailSendCodeView.as_view(), name='user_send_verify_code'),
    # 用户保存邮箱修改
    path('email_modify/save/', SaveEmailModifyView.as_view(), name='user_save_email_modify'),
    # 我的课程
    path("mycourse/", MyCourseView.as_view(), name='mycourse'),

    # 我的收藏--课程机构
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    # 我的收藏--授课教师
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我的收藏--公开课程
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),

    # # 我的消息
    # path('my_message/', MyMessageView.as_view(), name="my_message"),
]
