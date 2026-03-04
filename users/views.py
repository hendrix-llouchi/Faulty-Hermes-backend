from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from .models import UserProfile
from .serializers import UserRegistrationSerializer, LeaderboardSerializer

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserProfile.objects.order_by('-xp')[:10]


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
