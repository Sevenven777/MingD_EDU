# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 2:21 PM'

import xadmin
from .models import *
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '铭德教育后台管理系统'
    site_footer = '铭德教育在线课堂'
    menu_style = 'accordion'


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'add_time']
    model_icon = 'fa fa-code'


# class BannerInfoXadmin(object):
#     list_display = ['title', 'image', 'url', 'index', 'add_time']
#     search_fields = ['title', 'image', 'url', 'index']
#     list_filter = ['title', 'image', 'url', 'index', 'add_time']
#     model_icon = 'fa fa-file-image-o'


xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)
# xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
