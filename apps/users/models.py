# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nike_name = models.CharField(max_length=50, verbose_name="昵称", default="", blank=True)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(("male", '男'), ("female", '女')), default="female", max_length=20)
    address = models.CharField(max_length=100, default='', blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="media/image/%Y/%m", default="media/image/default.png", max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=200, verbose_name="邮箱")
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')), verbose_name="验证码类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name


class BannerInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name="轮播图片", max_length=200)
    url = models.URLField(max_length=200, verbose_name="图片链接")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.image)
