# apps/utils/email_send.py

from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from online_edu.settings import EMAIL_FROM


# 生成验证邮箱用的随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 注册邮箱验证
def send_register_eamil(email, send_type="register"):
    # 将邮箱验证的数据保存数据库
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件发送的内容:
    email_title = ""
    email_body = ""

    # 注册时邮件内容
    if send_type == "register":
        email_title = "ABL在线教育平台注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        # 通过Django提供的方法来发送邮件，在这之前需setting.py进行配置
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
    elif send_type == "forget":  # 找回密码时邮件内容
        email_title = "ABL在线教育平台找回密码链接"
        email_body = "请点击下面的链接修改你的密码: http://127.0.0.1:8000/reset/{0}".format(code)

        # 通过Django提供的方法来发送邮件，在这之前需setting.py进行配置
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
