from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, ReCommentForm
from .models import Post, Comment, ReComment, PostLike, CommentLike, ReCommentLike
from django.contrib.auth.decorators import login_required

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
