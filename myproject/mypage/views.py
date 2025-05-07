from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Post 

@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(writer=user).order_by('-id')
    
    context = {
        'posts' : posts,
        'user' : user
    }
    
    return render(request, 'mypage.html', context)