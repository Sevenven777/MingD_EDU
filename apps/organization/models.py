# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime


# Create your models here.
class CityInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名称")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=20, verbose_name="机构名称")
    desc = models.CharField(max_length=200, verbose_name="机构简介")
    click_num = models.IntegerField(default=0, verbose_name="访问量")
    fav_num = models.IntegerField(default=0, verbose_name="收藏数")
    address = models.CharField(max_length=200, verbose_name="机构地址")
    image = models.ImageField(upload_to='org/%Y/%m', default="", max_length=200, verbose_name="机构封面")
    course_num = models.IntegerField(default=0, verbose_name="课程数")
    study_num = models.IntegerField(default=0, verbose_name="学习人数")
    cityinfo = models.ForeignKey(CityInfo, verbose_name="所在城市", on_delete=models.CASCADE)

    # detail = UEditorField(verbose_name='机构详情',
    #                       width=700,
    #                       height=400,
    #                       toolbars='full',
    #                       imagePath='ueditor/images/',
    #                       filePath='ueditor/files/',
    #                       upload_settings={'imageMaxSizing': 1024000},
    #                       default='')
    #
    category = models.CharField(choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')), max_length=20,
                                default='pxjg', verbose_name="机构类别")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '机构信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        # 获取课程机构的教师数量
        return self.teacher_set.all().count()


class Teacher(models.Model):
    name = models.CharField(max_length=20, verbose_name="教师姓名")
    work_year = models.IntegerField(default=3, verbose_name="工作年限")
    work_company = models.CharField(max_length=20, verbose_name="就职公司")
    work_position = models.CharField(max_length=20, verbose_name="工作职位")
    work_style = models.CharField(max_length=20, verbose_name="教学特点")
    love_num = models.IntegerField(default=0, verbose_name="收藏数")
    click_num = models.IntegerField(default=0, verbose_name="访问量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="teacher/%Y/%m", default="", max_length=100, verbose_name="头像")
    # image = models.ImageField(upload_to='teacher/', max_length=200, verbose_name="讲师头像")
    age = models.IntegerField(default=30, verbose_name="讲师年龄")

    # gender = models.CharField(choices=(('boy', '男'), ('girl', '女')), max_length=10, verbose_name="讲师性别", default='boy')

    class Meta:
        verbose_name = '讲师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
