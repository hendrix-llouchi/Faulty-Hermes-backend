from django.db import models


class UserProfile(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True)
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True)
    profile_photo_url = models.URLField(blank=True)
    interests = models.JSONField(default=list)
    streak_days = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return self.username
