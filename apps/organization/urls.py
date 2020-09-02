# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/18/2020 9:40 AM'

from django.urls import path, include, re_path

from organization.views import *

urlpatterns = [
    # 课程机构列表页
    path(r'list/', OrgView.as_view(), name="org_list"),
    path(r'add_ask/', AddUserAskView.as_view(), name="add_ask"),
    path(r'home/(?P<org_id>\d+)', OrgHomeView.as_view(), name="org_home"),
    path(r'course/(?P<org_id>\d+)', OrgCourseView.as_view(), name="org_course"),
    path(r'desc/(?P<org_id>\d+)', OrgDescView.as_view(), name="org_desc"),
    path(r'org_teacher/(?P<org_id>\d+)', OrgTeachercView.as_view(), name="org_teacher"),
    # 用户收藏
    path(r'add_fav/', AddFavView.as_view(), name="add_fav"),

    # 讲师列表页
    path(r'teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情页
    path(r'teacher/detail/(?P<teacher_id>\d+)', TeacherDetailView.as_view(), name="teacher_detail"),

    # path(r'myhome/(?P<org_id>\d+)', OrgHomeView.as_view(), name="myhome"),
]
