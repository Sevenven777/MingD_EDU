# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/16/2020 5:01 PM'

from django import forms
from captcha.fields import CaptchaField

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少8位',
        'max_length': '密码不能超过20位'
    })


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8, error_messages={
        'min_length': '密码至少8位'
    })
    captcha = CaptchaField(error_messages={"invalid": "验证码错误！"})


class FogetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误！"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8,error_messages={"invalid": "密码输入错误！"})
    password2 = forms.CharField(required=True, min_length=8,error_messages={"invalid": "密码输入错误！"})


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nike_name', 'gender', 'birthday', 'address', 'mobile']


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nike_name', 'gender', 'birthday', 'address', 'mobile']


class ModifyMailForm(forms.Form):
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True)