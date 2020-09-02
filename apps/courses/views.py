# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import *
from operation.models import *
from utils.mixin_utils import *


# Create your views here.

class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 15, request=request)

        courses = p.page(page)
        courses_num = all_courses.count()
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
            'courses_num': courses_num,
        })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加点击数
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=2):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=1):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not user_courses:
            user_course = UserCourse(study_man=request.user, study_course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(study_course=course)
        user_ids = [user_course.study_man.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(study_man_id__in=user_ids)
        course_ids = [user_course.study_course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]
        all_resources = SourceInfo.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses

        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not user_courses:
            user_course = UserCourse(study_man=request.user, study_course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(study_course=course)
        user_ids = [user_course.study_man.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(study_man_id__in=user_ids)
        course_ids = [user_course.study_course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]

        all_resources = SourceInfo.objects.filter(course=course)
        all_comments = UserComment.objects.filter(comment_course_id=course.id).order_by("-add_time")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_comments, 10, request=request)

        comments = p.page(page)
        comment_nums = all_comments.count()

        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': comments,
            'relate_courses': relate_courses,
            'comment_nums': comment_nums,
        })


class AddCommentView(View):
    """
    用户添加课程评论
    """

    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = int(request.POST.get("course_id", 0))
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comment = UserComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.comment_course = course
            course_comment.comment_content = comments
            course_comment.comment_man = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(study_man=request.user, study_course=course)
        if not user_courses:
            user_course = UserCourse(study_man=request.user, study_course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(study_course=course)
        user_ids = [user_course.study_man.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(study_man_id__in=user_ids)
        course_ids = [user_course.study_course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_num")[:5]
        all_resources = SourceInfo.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video

        })
