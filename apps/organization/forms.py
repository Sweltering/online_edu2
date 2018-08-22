import re

from django import forms

from operation.models import UserAsk


# django的model验证form表单
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 实例化UserAskForm时就验证手机号码
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']  # 取出mobile
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
