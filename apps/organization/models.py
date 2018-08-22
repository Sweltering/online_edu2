from datetime import datetime

from django.db import models


# Create your models here.

# 城市相关信息
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="城市添加时间")

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    # 后台管理系统显示的名字
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# 课程机构相关信息
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20, default='pxjg',
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), verbose_name='机构类别')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to='org/%Y/%m', max_length=100, verbose_name="logo")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u"所在城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="机构添加时间")
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# 教师相关信息，与机构是一对多的关系
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='教师添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师: {1}".format(self.org, self.name)
