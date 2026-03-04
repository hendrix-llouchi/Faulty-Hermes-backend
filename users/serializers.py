from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserProfile

class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'xp', 'streak_days']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    target_lang = serializers.CharField(write_only=True, required=True, max_length=10)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'target_lang']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        # Extract target_lang before passing to User creation
        target_lang = validated_data.pop('target_lang')
        validated_data['password'] = make_password(validated_data['password'])
        
        # User is created here. The signal in users/signals.py automatically creates the UserProfile
        user = super().create(validated_data)
        
        # Update the implicitly created profile with the requested target language
        user.profile.target_lang = target_lang
        user.profile.save()
        
        return user
