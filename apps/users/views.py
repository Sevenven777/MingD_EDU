# coding=utf-8
import json
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from pure_pagination import Paginator

from courses.models import Course
from operation.models import UserFavorite, UserCourse, UserMessage
from organization.models import CourseOrg, CityInfo, Teacher
from .forms import *
from apps.utils.email_send import *
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_recodes = EmailVerifyCode.objects.filter(code=active_code)
        if all_recodes:
            for record in all_recodes:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "register.html")

        return render(request, "login.html")


# class RegisterView(View):
#     def get(self, request):
#         register_form = RegisterForm()
#         return render(request, "register.html", {'register_form': register_form})
#
#     def post(self, request):
#         register_form = RegisterForm(request.POST)
#         if register_form.is_valid():
#             user_mail = request.POST.get("email", "")
#             user_name = request.POST.get("username", "")
#             if UserProfile.objects.filter(email=user_mail):
#                 return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在！"})
#             pass_word = request.POST.get("password", "")
#             user_profile = UserProfile()
#             user_profile.nike_name = user_name
#             user_profile.username = user_name
#             user_profile.email = user_mail
#             user_profile.is_active = False
#             user_profile.password = make_password(pass_word)
#             user_profile.save()
#
#             send_register_emall(user_mail, 1)
#             return render(request, "login.html")
#         else:
#             return render(request, "register.html", {"register_form": register_form})
#
#
# class LoginView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "login.html", {})
#
#     def post(self, request, *args, **kwargs):
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user_name = request.POST.get("username", "")
#             pass_word = request.POST.get("password", "")
#             # 通过用户名和密码查询用户是否存在
#             user = authenticate(username=user_name, password=pass_word)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return render(request, "index222.html")
#                 else:
#                     return render(request, "login.html", {"msg": "用户未激活！"})
#             else:
#                 return render(request, "login.html", {"msg": "用户名或密码错误！"})
#
#         else:
#             return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """
    登出视图
    """

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self, request):
        forget_form = FogetForm()
        return render(request, "fgtpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = FogetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_emall(email, 2)
            return render(request, "login.html")
        else:
            return render(request, "fgtpwd.html", {"forget_form": forget_form})


class ResetView(View):
    """
    重置密码
    """
    def get(self, request, active_code):
        all_recodes = EmailVerifyCode.objects.filter(code=active_code)
        if all_recodes:
            for record in all_recodes:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            # active_fail.html
            return render(request, "register.html")

        return render(request, "login.html")


class ModifyPwdView(View):
    """
    未登录用户修改密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        user_info_form = UserInfoForm()
        return render(request, "usercenter-info.html", {
            'user_info_form': user_info_form
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)

        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserInfoChangeView(LoginRequiredMixin, View):
    """
    用户修改个人信息
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', locals())

    def post(self, request):
        user_center_info_form = UserChangeInfoForm(request.POST, instance=request.user)  # 传递一个user实例，否则是新增，而不是修改
        if user_center_info_form.is_valid():
            if len(user_center_info_form.mobile) < 11:
                return HttpResponse('{"change_info":"failure", "info_save__msg":"电话号码长度出错！"}',
                                    content_type='application/json')
            user_center_info_form.save()
            return HttpResponse('{"change_info":"success", "info_save__msg":"用户信息更新成功"}',
                                content_type='application/json')
        else:
            user_center_info_errors = json.dumps(user_center_info_form.errors, ensure_ascii=False)
            return HttpResponse(user_center_info_errors, content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def save_file(self, file):
        with open("../../media/head_images/uploaded.jpg", "wb") as f:
            for chunk in file.chuncks():
                f.write(chunk)

    def post(self, request):
        # files = request.FILES["images"]
        # self.save_file(files)
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"update_image":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"update_image":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    在个人中心修改密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"modify_pwd":"fail","msg":"密码不一致！"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"modify_pwd":"success","msg":"修改成功！"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class Login_RegisterView(View):
    """
    登录
    """
    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        return render(request, "login.html", {'register_form': register_form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 通过用户名和密码查询用户是否存在
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})

        else:
            return render(request, "login.html", {"login_form": login_form})


class Register_View(View):
    """
    注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            user_mail = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_mail):
                return HttpResponse('{"status":"fail", "msg":"用户已经存在"}', content_type='application/json')
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.nike_name = user_name
            user_profile.username = user_name
            user_profile.email = user_mail
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_emall(user_mail, 1)
            return render(request, "register.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        user_courses = UserCourse.objects.filter(study_man=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课教师
    """

    def get(self, request):
        teacher_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            teacher_id = fav_org.fav_id
            # 获取这个机构对象
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """

    def get(self, request):
        course_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            course_id = fav_org.fav_id
            # 获取这个机构对象
            course = Course.objects.get(id=course_id)

            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
        })


# class MyMessageView(LoginRequiredMixin, View):
#     '''我的消息'''
#
#     def get(self, request):
#         all_message = UserMessage.objects.filter(user=request.user.id)
#
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#         p = Paginator(all_message, 4, request=request)
#         messages = p.page(page)
#         return render(request, "usercenter-message.html", {
#             "messages": messages,
#         })


class ModifyEmailSendCodeView(LoginRequiredMixin, View):
    """
    个人中心修改邮箱发送验证码
    """
    def get(self, request):
        new_email = request.GET.get('new_email', '').strip()
        if new_email == '':
            return HttpResponse('{"email_status":"fail", "email_msg":"邮箱不能为空"}', content_type='application/json')
        elif UserProfile.objects.filter(email=new_email):
            return HttpResponse('{"email_status":"fail", "email_msg":"邮箱已存在"}', content_type='application/json')
        else:
            if send_register_emall(new_email, 3):
                return HttpResponse('{"email_status":"success", "email_msg":"邮件发送成功，请注意查收"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"email_status":"fail", "email_msg":"邮箱可能格式错误，发送失败"}',
                                    content_type='application/json')


# 保存修改的邮箱
class SaveEmailModifyView(LoginRequiredMixin, View):
    """
    保存用户修改的邮箱
    """
    def post(self, request):
        modify_mail_form = ModifyMailForm(request.POST)
        if modify_mail_form.is_valid():
            new_email = request.POST.get('email', '')
            verification_code = request.POST.get('code', '')

            # 查询验证码是否存在

            existed_record = EmailVerifyCode.objects.filter(code=verification_code, email=new_email, send_type=3)

            if existed_record:
                user = request.user
                user.email = new_email
                user.save()
                return HttpResponse('{"save_email_status":"success", "save_email_msg":"邮箱已更新"}',
                                    content_type='application/json')
            else:
                return HttpResponse('{"save_email_status":"fail", "save_email_msg":"验证码错误！"}',
                                    content_type='application/json')
        else:
            return HttpResponse('{"save_email_status":"fail", "save_email_msg":"邮箱验证失败"}',
                                content_type='application/json')


# class Test(View):
#
#     def get(self, request):
#         """
#         课程机构列表功能
#         :param request:
#         :return:
#         """
#         all_orgs = CourseOrg.objects.all()
#         hot_orgs = all_orgs.order_by("click_num")[:3]
#
#         all_citys = CityInfo.objects.all()
#
#         # 机构搜索
#         search_keywords = request.GET.get('keywords', "")
#         if search_keywords:
#             all_orgs = all_orgs.filter(
#                 Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
#
#         city_id = request.GET.get('city', "")
#
#         if city_id:
#             all_orgs = all_orgs.filter(cityinfo_id=int(city_id))
#
#         category = request.GET.get('ct', "")
#         if category:
#             all_orgs = all_orgs.filter(category=category)
#
#         sort = request.GET.get('sort', "")
#         if sort:
#             if sort == "study_num":
#                 all_orgs = all_orgs.order_by("-study_num")
#             elif sort == "course_num":
#                 all_orgs = all_orgs.order_by("-course_num")
#
#         # 对课程机构进行分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#
#         p = Paginator(all_orgs, 5, request=request)
#
#         orgs = p.page(page)
#         org_nums = all_orgs.count()
#
#         return render(request, 'org_list.html', {
#             "all_orgs": orgs,
#             "all_citys": all_citys,
#             "org_nums": org_nums,
#             "city_id": city_id,
#             "category": category,
#             "hot_orgs": hot_orgs,
#             "sort": sort
#         })
