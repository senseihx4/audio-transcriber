from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from ailock.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        (1, 'SuperAdmin'),
        (2, 'Admin'),
        (3, 'User'),
    )

    user_type = models.PositiveSmallIntegerField(
    choices=USER_TYPES,
    default=3
     )
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class audiotext(models.Model):
    audio_file = models.FileField(upload_to='audio_files/')
    record_audiofile = models.FileField(upload_to='record_audiofiles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


    def __str__(self):
        return f"AudioText for {self.user.email}"
    


class yotubeaudio(models.Model):
    youtube_url = models.URLField()
    record_audiofile = models.FileField(upload_to='record_youtubeaudiofiles/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"YouTubeAudio for {self.user.email}"