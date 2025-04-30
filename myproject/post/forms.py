from django import forms
from .models import Post, Comment, ReComment, Search

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'link', 'stack']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment
        fields = ['recomment']
        
class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['title']
