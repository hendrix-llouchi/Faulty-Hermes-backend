from django.urls import path
from .views import RegisterView, LeaderboardViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('leaderboard/', LeaderboardViewSet.as_view({'get': 'list'}), name='leaderboard'),
]
# Force reload
