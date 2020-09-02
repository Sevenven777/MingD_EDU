# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 2:56 PM'

import xadmin
from .models import *


class CityInfoXadmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-bars'


class CourseOrgXadmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num']
    search_fields = ['name', 'desc', 'click_num', 'fav_num']
    list_filter = ['name', 'desc', 'click_num', 'fav_num']
    model_icon = 'fa fa-hdd-o'


class TeacherInfoXadmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company']
    search_fields = ['org', 'name', 'work_year', 'work_company']
    list_filter = ['org', 'name', 'work_year', 'work_company']
    model_icon = 'fa fa-female'

xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(CourseOrg, CourseOrgXadmin)
xadmin.site.register(Teacher, TeacherInfoXadmin)
