from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import base64
import uuid
from django.core.files.base import ContentFile


class Design(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='designs/')  
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name='likes', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'design')  

    def __str__(self):
        return f"{self.user.username} liked {self.design.title}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} on {self.design.title}: {self.content[:20]}..."

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('follower', 'followed') 

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    

class CapturedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='captured_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save_base64_image(self, base64_string):
        """Convert base64 to an image file and save it."""
        format, imgstr = base64_string.split(';base64,')  
        ext = format.split('/')[-1] 
        file_name = f"{uuid.uuid4()}.{ext}" 
        self.image.save(file_name, ContentFile(base64.b64decode(imgstr)), save=True)

