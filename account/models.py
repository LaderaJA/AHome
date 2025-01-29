from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
