# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 3:02 PM'

import xadmin
from .models import *


# class UserAskXadmin(object):
#     list_display = ['name', 'phone', 'course', 'add_time']
#     search_fields = ['name', 'phone', 'course']
#     list_filter = ['name', 'phone', 'course', 'add_time']
#     model_icon = 'fa fa-envelope-o'


class UserCourseXadmin(object):
    list_display = ['study_man', 'study_course', 'add_time']
    search_fields = ['study_man', 'study_course']
    list_filter = ['study_man', 'study_course', 'add_time']
    model_icon = 'fa fa-bookmark-o'


class UserFavoriteXadmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-heart-o'


class UserCommentXadmin(object):
    list_display = ['comment_man', 'comment_course', 'comment_content', 'add_time']
    search_fields = ['comment_man', 'comment_course', 'comment_content']
    list_filter = ['comment_man', 'comment_course', 'comment_content', 'add_time']
    model_icon = 'fa fa-comments'


# class UserMessageXadmin(object):
#     list_display = ['user', 'message', 'has_read', 'add_time']
#     search_fields = ['user', 'message', 'has_read']
#     list_filter = ['user', 'message', 'has_read', 'add_time']
#     model_icon = 'fa fa-comment-o'


# xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserFavorite, UserFavoriteXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
# xadmin.site.register(UserMessage, UserMessageXadmin)
