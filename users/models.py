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
    last_activity_date = models.DateField(null=True, blank=True)
    target_lang = models.CharField(max_length=10, default='en')  # Added for chat translation
    def __str__(self):
        return self.user.username


class UserConnection(models.Model):
    """Tracks who has added whom as a contact."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_contacts')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'contact']

    def __str__(self):
        return f"{self.user.username} → {self.contact.username}"
