# users/adminx.py

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


# 后台注册邮箱验证表
class EmailVerifyRecordAdmin(object):
    # 后台用户信息显示的字段有哪些
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索功能
    search_fields = ['code', 'email', 'send_type']
    # 过滤功能
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 后台注册轮播图
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 后台主题样式配置
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# logo和底部，以及菜单收起配置
class GlobalSettings(object):
    # 修改title
    site_title = 'ABL后台管理系统'
    # 修改footer
    site_footer = 'ABL@2018'
    # 收起菜单
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
