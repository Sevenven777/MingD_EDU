# Generated by Django 2.2.3 on 2020-05-20 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20200518_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=30, verbose_name='讲师年龄'),
        ),
    ]
