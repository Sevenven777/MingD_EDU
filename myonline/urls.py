"""myonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import *
from organization.views import *
from myonline.settings import *
from courses.views import *

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    # 首页
    path(r'', TemplateView.as_view(template_name="index.html"), name="index"),

    # path(r'login/', LoginView.as_view(), name="login"),
    # 登录页面
    path(r'login/', Login_RegisterView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 注册页面
    path(r'register/', Register_View.as_view(), name="register"),
    # path(r'register/', RegisterView.as_view(), name="register"),
    # 验证码
    path(r'captcha/', include('captcha.urls')),
    re_path(r'active/(?P<active_code>[a-zA-Z0-9]+)', ActiveUserView.as_view(), name="user_active"),
    # 忘记密码
    path(r'forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    # 重置密码
    re_path(r'reset/(?P<active_code>[a-zA-Z0-9]+)', ResetView.as_view(), name="reset_pwd"),

    path(r'modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    # 课程机构url配置
    path(r'org/', include(('organization.urls', 'organization'), namespace="org")),
    # 课程相关url配置
    path(r'courses/', include(('courses.urls', 'organization'), namespace="courses")),
    # 配置上传文件的访问处理函数
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # path(r'index/', TemplateView.as_view(template_name="index222.html"), name="index")
    path(r'users/', include(('users.urls', 'organization'), namespace="users")),

    # path(r'test/', Test.as_view(), name="test"),
]
