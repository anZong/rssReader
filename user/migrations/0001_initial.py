# Generated by Django 2.1 on 2018-08-22 08:09

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
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('ordering', models.IntegerField(default=0, verbose_name='排序')),
                ('username', models.TextField(blank=True, editable=False, max_length=32, null=True, unique=True, verbose_name='用户名')),
                ('password', models.TextField(blank=True, max_length=128, null=True, verbose_name='密码')),
                ('nickname', models.TextField(default='', max_length=32, verbose_name='昵称')),
                ('phone', models.TextField(blank=True, max_length=11, null=True, verbose_name='手机号码')),
                ('email', models.EmailField(blank=True, max_length=32, null=True, verbose_name='邮箱')),
                ('openid', models.TextField(default='', verbose_name='微信openid')),
                ('avatar', models.TextField(default='', verbose_name='头像')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('country', models.TextField(default='', verbose_name='国家')),
                ('province', models.TextField(default='', verbose_name='省份')),
                ('city', models.TextField(default='', verbose_name='城市')),
                ('age', models.IntegerField(default=18, verbose_name='年龄')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['id'],
            },
        ),
    ]
