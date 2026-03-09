from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny] # Allow for testing

    def get_queryset(self):
        # For now, return all messages so they can see everything during testing
        return Message.objects.all()

    def perform_create(self, serializer):
        # For testing: if sender is provided in request data, use it.
        # Otherwise use the authenticated user.
        sender_username = self.request.data.get('sender')
        
        if sender_username:
            try:
                sender = User.objects.get(username=sender_username)
                serializer.save(sender=sender)
            except User.DoesNotExist:
                raise ValidationError(detail={"error": f"Sender user '{sender_username}' not found"})
        elif self.request.user.is_authenticated:
            serializer.save(sender=self.request.user)
        else:
            raise ValidationError(detail={"error": "Sender not specified and user not logged in"})
