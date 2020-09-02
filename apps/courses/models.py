# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from organization.models import *


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=20, verbose_name="课程名称")
    desc = models.CharField(max_length=200, verbose_name="课程简介")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=(('gj', '高级'), ('zj', '中级'), ('cj', '初级')), max_length=5, verbose_name="课程难度",
                              default='cj')
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=200, verbose_name="课程封面")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    category = models.CharField(choices=(('qd', '前端开发'), ('hd', '后端开发')), verbose_name="课程类别", max_length=25,
                                default="后端开发")
    course_notice = models.CharField(max_length=200, verbose_name="课程公告",default="新公告")
    course_need = models.CharField(max_length=100, verbose_name="课程须知",default="")
    teacher_tell = models.CharField(max_length=100, verbose_name="老师教导",default="")
    course_org = models.ForeignKey(CourseOrg, verbose_name="所属机构", null=True, blank=True, on_delete=models.SET_NULL)
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)

    teacher = models.ForeignKey(Teacher, verbose_name="讲师",null=True,blank=True,on_delete=models.SET_NULL)
    # is_banner = models.BooleanField(default=False, verbose_name="是否轮播")

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    # 章节数
    def get_zj_numbers(self):
        return self.lesson_set.all().count()

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return self.name





class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="章节名称")
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_vedio(self):
        # 获取课程所有章节视频
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=50, verbose_name="视频名称")
    study_time = models.IntegerField(default=0, verbose_name="视频时长")
    file_upload = models.FileField(upload_to="media/video/%Y/%m", verbose_name="视频", max_length=200)
    lesson = models.ForeignKey(Lesson, verbose_name="所属章节", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SourceInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="资源名称")
    down_load = models.FileField(upload_to='media/source/%Y/%m', max_length=200, verbose_name="下载路径")
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '资源信息'
        verbose_name_plural = verbose_name


