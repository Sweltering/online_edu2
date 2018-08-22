from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm


# Create your views here.

# 课程机构列表功能
class OrgView(View):
    def get(self, request):
        # 查询所有机构和城市的字段信息
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        # 机构热门排序
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 学习人数、课程数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 统计后台机构的数量
        org_nums = all_orgs.count()

        # 使用第三方库pure-pagination对机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html", {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


# 我要学习表单提交功能
class AddUserAskView(View):
    def post(self, request):
        # 提交表单验证
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():  # 表单验证通过，继续提交
            user_ask = userask_form.save(commit=True)  # model表单验证可以直接将提交的内容保存数据库

            # 前端AJAX异步提交数据，返回json数据
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')
