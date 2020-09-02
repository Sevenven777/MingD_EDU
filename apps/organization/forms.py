# -*- coding:utf-8 -*-
__author__ = 'TianTiantian'
__date__ = '5/18/2020 9:36 AM'

import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        p = re.compile(r"^1[35678]\d{9}$")
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError("手机号码非法", code="moblie_invalid")
