from django.db import models
from user.models import CustomUser

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Visit(models.Model):
    profile_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visits_received')
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='visits_written')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)