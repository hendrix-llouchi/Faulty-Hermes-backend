from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender='lessons.UserProgress')
def award_xp_on_lesson_completion(sender, instance, created, **kwargs):
    """
    Awards XP to the user's profile when a lesson is marked as completed.
    The `created` guard ensures XP is only added the first time, preventing
    XP farming from repeated calls for the same lesson.
    """
    if created and instance.is_completed:
        xp_reward = instance.lesson.xp_reward
        UserProfile.objects.filter(user=instance.user).update(
            xp=models.F('xp') + xp_reward
        )
