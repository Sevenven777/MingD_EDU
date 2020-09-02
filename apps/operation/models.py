# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from users.models import *
from courses.models import Course


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="手机")
    course = models.CharField(max_length=20, verbose_name="课程名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '咨询信息'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="收藏用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name="收藏id")
    fav_type = models.IntegerField(choices=((1, '机构'), (2, '课程'), (3, '讲师')), default=1, verbose_name="收藏类别")
    # fav_status = models.BooleanField(default=False, verbose_name="收藏状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserCourse(models.Model):
    study_man = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    study_course = models.ForeignKey(Course, verbose_name="学习课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="学习时间")

    class Meta:
        unique_together = ('study_man', 'study_course')
        verbose_name = '用户学习课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.study_man.username


class UserComment(models.Model):
    comment_man = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    comment_course = models.ForeignKey(Course, verbose_name="评论课程", on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300, verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment_man.username


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户")  # 默认为0发给所有的用户
    message = models.CharField(max_length=200, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name
