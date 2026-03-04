from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'original_text', 'translated_text', 'timestamp']
        read_only_fields = ['sender', 'translated_text']
