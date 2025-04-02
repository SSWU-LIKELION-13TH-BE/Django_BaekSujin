from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import CustomUser

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'login.html')
        
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('user:main')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    auth.logout(request)
    return redirect('user:login')

def main_view(request):
    return render(request, 'main.html')

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
