from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Video(models.Model):
    title = models.CharField(max_length=200)
    # SubtitleFile = models.CharField(max_length=200, default="")
    file = models.FileField(upload_to='videos/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=10, default='en')
    text = models.TextField()
    timestamp = models.CharField(max_length=50)

