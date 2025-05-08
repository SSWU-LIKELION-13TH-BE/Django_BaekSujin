from post.models import Post, CustomUser
from .forms import VisitForm
from .models import Visit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(writer=user).order_by('-id')
    
    context = {
        'posts' : posts,
        'user' : user
    }
    
    return render(request, 'mypage.html', context)

@login_required
def go_mypage_view(request):
    user = request.user
    posts = Post.objects.filter(writer=user).order_by('-id')
    visits = Visit.objects.filter(profile_owner=user, writer=request.user)
    
    context = {
        'posts': posts,
        'user': user,
        'visits': visits,
    }
    return render(request, 'mypage.html', context)


@login_required
def visit_view(request, user_id):
    owner = get_object_or_404(CustomUser, id=user_id)
    posts = owner.post_set.all()

    if request.method == 'POST':  # 방명록 폼 입력 시
        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            visit = visit_form.save(commit=False)
            visit.writer = request.user
            visit.profile_owner = owner
            visit.save()
            return redirect('mypage:visit', user_id=user_id)  # 다시 해당 유저의 마이페이지로 리다이렉트
    else:
        visit_form = VisitForm()

    visits = Visit.objects.filter(profile_owner=owner)
    # profile_owner는 마이페이지 주인을 기준으로 방명록을 불러옵니다.

    context = {
        'profile_owner': owner,
        'posts': posts,
        'visit_form': visit_form,
        'visits': visits
    }

    return render(request, 'visit_mypage.html', context)
