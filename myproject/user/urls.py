from django.urls import path
from .views import signup_view, login_view, logout_view, main_view, findPW_view

app_name = "user"

urlpatterns = [
    path('', main_view, name='main'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('findPW/', findPW_view, name='findPW'),
    
]