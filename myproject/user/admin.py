# user/admin.py

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.admin import SocialAppAdmin
from django.contrib import admin

class CustomSocialAppAdmin(SocialAppAdmin):
    def delete_model(self, request, obj):
        # 먼저 사이트 연결 끊기
        obj.sites.clear()  # 연결된 모든 사이트 삭제
        
        # 부모 클래스의 delete_model 호출하여 실제 삭제
        super().delete_model(request, obj)

# 이 CustomSocialAppAdmin을 사용하여 SocialApp 모델을 등록합니다.
admin.site.unregister(SocialApp)  # 기존 등록된 SocialApp 제거
admin.site.register(SocialApp, CustomSocialAppAdmin)  # CustomSocialAppAdmin 등록
