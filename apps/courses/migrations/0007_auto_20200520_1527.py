# Generated by Django 2.2.3 on 2020-05-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200520_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_need',
            field=models.CharField(default='', max_length=100, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=100, verbose_name='老师教导'),
        ),
    ]
