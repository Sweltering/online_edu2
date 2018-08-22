"""online_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
import xadmin
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from online_edu.settings import MEDIA_ROOT

urlpatterns = [
    # 登录注册相关URL
    path('xadmin/', xadmin.site.urls),  # 后台管理系统
    path("", TemplateView.as_view(template_name="index.html"), name="index"),  # 首页
    path("login/", LoginView.as_view(), name="login"),  # 登录
    path("register/", RegisterView.as_view(), name="register"),  # 注册
    path("captcha/", include("captcha.urls")),  # 验证码
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),  # 注册用户激活
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),  # 忘记密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),   # 修改密码

    # 课程机构相关URL
    url(r'^org/', include('organization.urls', namespace='org')),  # 课程机构
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})  # 配置上传文件的访问处理函数

]
