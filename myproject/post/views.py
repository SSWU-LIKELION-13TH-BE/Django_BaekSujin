from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, ReCommentForm
from .models import Post, Comment, ReComment, PostLike, CommentLike, ReCommentLike
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

def post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            return redirect('post:detail', post_id=post.id)
        else:
            return render(request, 'post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'post.html', {'form': form})

def detail_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm()
    recomment_form = ReCommentForm()
    context = {
        'post': post,
        'comments': post.comment_set.all().order_by('-created_at'),
        'comment_form': comment_form,
        'recomment_form': recomment_form,
    }
    
    post.views += 1
    post.save(update_fields=['views'])
    
    return render(request, 'postDetail.html', context)

@login_required
def comment_view(request, post_id):
    article = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.writer = request.user
        comment.save()
    return redirect('post:detail', post_id=article.id)

@login_required
def recomment_view(request, post_id):
    recomment_form = ReCommentForm(request.POST)
    if recomment_form.is_valid():
        recomment = recomment_form.save(commit=False)
        recomment.article = get_object_or_404(Post, pk=post_id)
        comment_id = request.POST.get("comment_id")
        recomment.comment = get_object_or_404(Comment, pk=comment_id)
        recomment.writer = request.user
        recomment.save()
    return redirect('post:detail', post_id=post_id)

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post:detail', post_id=post_id)

@login_required
def comment_like(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect('post:detail', post_id=post_id)

@login_required
def recomment_like(request, post_id, recomment_id):
    recomment = get_object_or_404(ReComment, pk=recomment_id)
    like, created = ReCommentLike.objects.get_or_create(recomment=recomment, user=request.user)
    if not created:
        like.delete()
    return redirect('post:detail', post_id=post_id)

# def search_view(request):
#     posts = Post.objects.all().order_by('-id')
    
#     q = request.POST.get('q', "")
    
#     if q:
#         posts = posts.filter(title__icontains=q)
#         return render(request, 'search.html', {'posts':posts, 'q':q})
#     else:
#         return render(request, 'postDetail.html')
    
def search_view(request):
    q = request.POST.get('q', "")
    # input name = 'p', 값이 없으면 기본값 빈 문자열!

    posts = Post.objects.filter(title__icontains=q).annotate(like_count=Count('likes')).order_by('-like_count', '-id')
    # Post 필드에 title에 q가 포함된 것, icontains:대문자 구분X
    # annotate : like_count라는 필드에 값 넣음 (Count 값 계산)
    # 정렬 1순위: 인기순, 2순위: 최신순
    
    if q:
        posts = posts.filter(title__icontains=q)
        return render(request, 'search.html', {'posts':posts, 'q':q})
    else:
        return render(request, 'postDetail.html')