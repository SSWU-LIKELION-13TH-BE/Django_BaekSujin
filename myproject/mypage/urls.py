from django.urls import path
from .views import profile_view, visit_view, go_mypage_view

app_name = "mypage"

urlpatterns = [
    path('', go_mypage_view, name='go_mypage'),
    path('profile/', profile_view, name='profile'),
    path('visit/<int:user_id>/', visit_view, name='visit'),
]
