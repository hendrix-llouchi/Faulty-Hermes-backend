from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True)
    profile_photo_url = models.URLField(blank=True)
    interests = models.JSONField(default=list)
    streak_days = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
