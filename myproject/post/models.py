from django.db import models
from user.models import CustomUser

CATEGORIES = (
    ('Python', 'Python'),
    ('C(or C++)', 'C(or C++)'),
    ('Java', 'Java')
)

class Post(models.Model):
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to="postImage/", blank=True, null=True)
    link = models.URLField(null=False)
    stack = models.CharField(max_length=10, choices=CATEGORIES)

    def __str__(self):
        return self.writer.username

class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ReComment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    recomment = models.TextField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.writer.username

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class ReCommentLike(models.Model):
    recomment = models.ForeignKey(ReComment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
