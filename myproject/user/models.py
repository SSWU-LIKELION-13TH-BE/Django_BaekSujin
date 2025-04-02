from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)