# Generated by Django 2.2.3 on 2020-05-16 13:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='城市名称')),
                ('desc', models.CharField(max_length=200, verbose_name='描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '城市信息',
                'verbose_name_plural': '城市信息',
            },
        ),
        migrations.CreateModel(
            name='CourseOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='机构名称')),
                ('desc', models.CharField(max_length=200, verbose_name='机构简介')),
                ('click_num', models.IntegerField(default=0, verbose_name='访问量')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('address', models.CharField(max_length=200, verbose_name='机构地址')),
                ('image', models.ImageField(max_length=200, upload_to='org/', verbose_name='机构封面')),
                ('course_num', models.IntegerField(default=0, verbose_name='课程数')),
                ('study_num', models.IntegerField(default=0, verbose_name='学习人数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('cityinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CityInfo', verbose_name='所在城市')),
            ],
            options={
                'verbose_name': '机构信息',
                'verbose_name_plural': '机构信息',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='教师姓名')),
                ('work_year', models.IntegerField(default=3, verbose_name='工作年限')),
                ('work_company', models.CharField(max_length=20, verbose_name='就职公司')),
                ('work_position', models.CharField(max_length=20, verbose_name='工作职位')),
                ('work_style', models.CharField(max_length=20, verbose_name='教学特点')),
                ('love_num', models.IntegerField(default=0, verbose_name='收藏数')),
                ('click_num', models.IntegerField(default=0, verbose_name='访问量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='所属机构')),
            ],
            options={
                'verbose_name': '讲师信息',
                'verbose_name_plural': '讲师信息',
            },
        ),
    ]