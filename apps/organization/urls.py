from django.conf.urls import url

from organization.views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView


app_name = 'org'

urlpatterns = [
    url(r"^list/$", OrgView.as_view(), name="org_list"),  # 课程机构页面
    url(r'^add_ask/', AddUserAskView.as_view(), name="add_ask"),  # 我要学习提交表单
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),  # 机构首页
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),  # 机构课程
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),  # 机构介绍
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),  # 机构介绍

]