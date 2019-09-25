# Generated by Django 2.0.7 on 2019-09-25 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='姓名')),
                ('password', models.CharField(blank=True, max_length=100, null=True, verbose_name='密码')),
                ('gender', models.CharField(blank=True, max_length=30, null=True, verbose_name='性别')),
                ('phonenumber', models.CharField(max_length=30, unique=True, verbose_name='手机号')),
                ('email', models.CharField(blank=True, max_length=50, null=True, verbose_name='邮箱')),
                ('company', models.CharField(blank=True, max_length=200, null=True, verbose_name='班级')),
                ('studentid', models.CharField(blank=True, max_length=30, null=True, verbose_name='学号')),
                ('about', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('registerdate', models.DateTimeField(auto_now_add=True, null=True, verbose_name='注册时间')),
                ('level', models.CharField(default='user', max_length=20, verbose_name='用户等级')),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]