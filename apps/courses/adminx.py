# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 2:45 PM'

import xadmin
from .models import *


# Create your models here.
class CourseXadmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


class LessonXadmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoXadmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class SourceInfoXadmin(object):
    list_display = ['course', 'name', 'down_load', 'add_time']
    search_fields = ['course', 'name', 'down_load']
    list_filter = ['course', 'name', 'down_load', 'add_time']


xadmin.site.register(Course, CourseXadmin)
xadmin.site.register(Lesson, LessonXadmin)
xadmin.site.register(Video, VideoXadmin)
xadmin.site.register(SourceInfo, SourceInfoXadmin)
