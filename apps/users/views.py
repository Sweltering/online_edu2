from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_eamil


# 重写Django后台的authenticate，可以让用户名和邮箱都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 查询用户是否存在
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 验证密码
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录功能
class LoginView(View):
    # GET方法进入
    def get(self, request):
        return render(request, 'login.html')

    # POST方法进入
    def post(self, request):
        # form表单预先验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 前端验证没有错误，会返回True，继续后端验证
            # 从表单中获取用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)

            # 验证用户名和密码
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:  # 验证通过
                if user.is_active:  # 只有注册激活才能登陆
                    login(request, user)
                    return render(request, 'index.html')
                else:  # 验证不通过
                    return render(request, 'login.html', {'msg': '用户名或密码错误!'})
        else:  # 前端验证不通过
            return render(request, "login.html", {"login_form": login_form})


# 注册功能
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        # form表单前端验证
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 验证没有错误返回True，继续后端注册
            user_name = request.POST.get('email', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象，注册信息存储到数据库
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False  # 表明用户还未激活
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name, 'register')
            return render(request, 'login.html')
        else:  # 前端验证失败
            return render(request, 'register.html', {'register_form': register_form})


# 用户点击激活链接激活用户
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        # 验证失败的时候跳转到激活失败页面
        else:
            return render(request, 'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html")


# 找回密码功能实现
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送邮件
            send_register_eamil(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 用户点击邮件链接进入修改密码页面
class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 返回到修改密码的页面
                return render(request, "password_reset.html", {"email": email})
        # 验证失败的时候跳转到激活失败页面
        else:
            return render(request, 'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html")


# 修改密码
class ModifyPwdView(View):
    def post(self, request, ):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:  # 修改时两次密码不相等，返回原页面
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})

            # 密码修改完成后修改数据库中原来的密码
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:  # form验证失败
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})
