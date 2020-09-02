# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/19/2020 5:49 PM'

from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # 课程列表页
    path(r'list/', CourseListView.as_view(), name="course_list"),

    # 热门课程推荐
    path(r'detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name="course_detail"),

    path(r'info/(?P<course_id>\d+)', CourseInfoView.as_view(), name="course_info"),

    path(r'comment/(?P<course_id>\d+)', CommentsView.as_view(), name="course_comment"),
    path(r'add_comment/', AddCommentView.as_view(), name="add_comment"),
    path(r'video/(?P<video_id>\d+)', VideoPlayView.as_view(), name="video_play"),

]
