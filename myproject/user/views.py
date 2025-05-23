from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, login as auth_login, update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm
from .models import CustomUser
from mypage.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from allauth.socialaccount.models import SocialApp

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)  # 새로 가입한 사용자를 로그인 처리

            return render(request, 'main.html')
        
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
    # SocialApp에서 provider를 필터링하여 첫 번째 항목만 가져오기
    social_providers = []
    for provider in ['naver', 'kakao']:  # 필터링할 provider 목록
        app = SocialApp.objects.filter(provider=provider).first()  # 첫 번째 항목만 가져오기
        if app:  # 해당 프로바이더가 존재하는 경우에만 추가
            social_providers.append({
                'id': app.id,
                'name': app.provider,
                'provider': app.provider
            })

    print(social_providers)  # social_providers 출력해서 확인

    # POST 요청일 경우 로그인 처리
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 사용자 인증
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return render(request, 'main.html')  # 로그인 성공 시 메인 페이지로 이동
        else:
            return render(request, 'login.html', {
                'error': '아이디 또는 비밀번호가 잘못되었습니다.',
                'social_providers': social_providers
            })

    # GET 요청일 경우 로그인 페이지 렌더링
    return render(request, 'login.html', {
        'social_providers': social_providers
    })
    
    
def logout_view(request):
    auth.logout(request)
    return redirect('user:login')

def main_view(request):
    profiles = Profile.objects.all() # Profile 모델을 통해 모든 프로필을 가져옵니다.
    return render(request, 'main.html', {'profiles': profiles})

def findPW_view(request):    
    if request.method == 'POST':
        username = request.POST['username'] # 변경시 확인용 아이디
        newPW = request.POST['newPW'] # 새 비밀번호
        newPW2 = request.POST['newPW2'] # 비밀번호 확인

        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)  # 유저 객체 가져오기
            # 삭제한 뒤 새로운 객체를 만들 필요없이, 객체의 기존 정보를 가져와서 수정!
            
            # PW - 해싱된 상태로 저장되므로 직접 접근이 불가
            # => 유저 객체를 가져와서 set_password를 사용하면(django 제공함수)
            # PW 삭제하지 않고 새로 저장할 수 있다.
            # password.delete()는 사용자 계정이 사라질 수 있으니 주의
            # CustomUser.objects.create()는 새로운 객체가 생성될 수 있으니 주의

            if newPW == newPW2:
                user.set_password(newPW)  # 비밀번호 변경
                user.save()  # 변경사항 저장
                return redirect('user:login')  # 비밀번호 변경 후 로그인 페이지로 이동
            else:
                return render(request, 'findPW.html', {"error": "비밀번호가 일치하지 않습니다."})
            
        else:
            return render(request, 'findPW.html', {"error": "존재하지 않는 아이디입니다."})
        
    return render(request, 'findPW.html')

@login_required
def update_view(request):
    if request.method == 'POST':
        upform = UserUpdateForm(request.POST, instance=request.user)
        # 현재 접속한 사용자로 접근하면 돼서 user.id 필요 X
        pwform = PasswordChangeForm(user=request.user, data=request.POST)
        
        if upform.is_valid() and pwform.is_valid():
            upform.save()
            user = pwform.save()
            update_session_auth_hash(request, user)  # ✅ 비밀번호 바꿔도 로그인 유지
            return redirect('user:main')        
    else:
        print('else')
        upform = UserUpdateForm(instance=request.user)
        pwform = PasswordChangeForm(user=request.user)
    return render(request, 'update.html', {'upform':upform, 'pwform':pwform})

@login_required
def toMypage_view(request):
    profiles = Profile.objects.exclude(user=request.user)  # 자기 자신 제외
    return render(request, 'main.html', {'profiles': profiles})