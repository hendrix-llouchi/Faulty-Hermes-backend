from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile, UserConnection
from .serializers import UserRegistrationSerializer, LeaderboardSerializer


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserProfile.objects.order_by('-xp')[:10]


class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.all().order_by('-id')
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UpdateProfileView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        username = request.data.get('username')
        target_lang = request.data.get('target_lang')
        if not username or not target_lang:
            return Response({'error': 'username and target_lang are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            profile.target_lang = target_lang
            profile.save()
            return Response({'success': True, 'username': username, 'target_lang': target_lang})
        except User.DoesNotExist:
            return Response({'error': f'User "{username}" not found'}, status=status.HTTP_404_NOT_FOUND)


class ContactsView(APIView):
    """
    GET  /api/v1/users/contacts/?username=X  → list of X's contacts
    POST /api/v1/users/contacts/             → {username, contact_username} → add contact
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username param required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        contacts = UserConnection.objects.filter(user=user).select_related('contact')
        data = [{'username': c.contact.username} for c in contacts]
        return Response(data)

    def post(self, request):
        username = request.data.get('username')
        contact_username = request.data.get('contact_username')
        if not username or not contact_username:
            return Response({'error': 'username and contact_username required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            contact = User.objects.get(username=contact_username)
        except User.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        connection, created = UserConnection.objects.get_or_create(user=user, contact=contact)
        if created:
            return Response({'success': True, 'message': f'Added {contact_username} to your contacts'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': True, 'message': 'Already in your contacts'})


class NewUsersView(APIView):
    """
    GET /api/v1/users/new/?username=X
    Returns users that X has NOT added as contacts yet (excluding self).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username param required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Users already added as contacts
        added_ids = UserConnection.objects.filter(user=user).values_list('contact_id', flat=True)
        # Return all users not in contacts and not self, newest first
        new_users = User.objects.exclude(id=user.id).exclude(id__in=added_ids).order_by('-date_joined')
        data = [{'username': u.username} for u in new_users]
        return Response(data)
