# Generated by Django 2.2.3 on 2020-05-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='study_time',
            field=models.IntegerField(default=0, verbose_name='视频时长'),
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='http://www.atguigu.com', verbose_name='视频链接'),
        ),
    ]