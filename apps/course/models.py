from datetime import datetime

from django.db import models

from organization.models import CourseOrg


# Create your models here.

# 课程相关的信息
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name="课程难度")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", max_length=100, verbose_name="封面图")
    click_nums = models.IntegerField(default=0, verbose_name="课程点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="课程添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # 后台章节里面是课程名称，一对多的关系
    def __str__(self):
        return self.name


# 章节相关的信息哦，与课程是一对多的关系，引入外键
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="章节添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


# 视频相关的信息，与章节是一对多的关系，引入外键
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="视频添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name


# 视频资源下载相关的信息，与课程是一对多的关系
class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="视频名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", max_length=100, verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="资源添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
