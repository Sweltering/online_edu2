from django.conf.urls import url

from organization.views import OrgView, AddUserAskView


app_name = 'org'

urlpatterns = [
    url(r"^list/$", OrgView.as_view(), name="org_list"),  # 课程机构页面
    url(r'^add_ask/', AddUserAskView.as_view(), name="add_ask")  # 我要学习提交表单
]