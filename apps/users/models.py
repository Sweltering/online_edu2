from django.db import models

# Create your models here.

# users/models.py

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户相关信息，继承AbstractUser父类中的一些字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default='', verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='female')
    adress = models.CharField(max_length=100, default='')  # 地址
    mobile = models.CharField(max_length=11, null=True, blank=True)  # 手机号
    image = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)  # 头像

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    # 打印的时候返回用户名，这个字段username继承自AbstractUser
    def __str__(self):
        return self.username


# 邮箱验证相关信息
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码')), max_length=30)  # 验证时的类型
    send_time = models.DateTimeField(default=datetime.now, verbose_name="验证时间")

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    # 后台显示邮箱验证添加内容后的名称
    def __str__(self):
        return "{}".format(self.email)


# 轮播图相关信息
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banner/%Y%m', max_length=100, verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
