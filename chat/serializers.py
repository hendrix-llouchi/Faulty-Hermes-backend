from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'original_text', 'translated_text', 'timestamp']
        read_only_fields = ['translated_text']
