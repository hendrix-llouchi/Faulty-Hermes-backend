from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp', 'streak_days', 'target_lang')
    # Explicitly including these fields to ensure they can be edited in the detail view
    fields = (
        'user', 
        'firebase_uid', 
        'bio', 
        'profile_photo_url', 
        'interests', 
        'xp', 
        'streak_days', 
        'last_activity_date', 
        'target_lang'
    )
