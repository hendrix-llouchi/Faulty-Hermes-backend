from django.urls import path
from .views import RegisterView, LeaderboardViewSet, UserListView, UpdateProfileView, ContactsView, NewUsersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('', UserListView.as_view(), name='user_list'),
    path('profile/', UpdateProfileView.as_view(), name='user_profile_update'),
    path('contacts/', ContactsView.as_view(), name='user_contacts'),
    path('new/', NewUsersView.as_view(), name='user_new'),
    path('leaderboard/', LeaderboardViewSet.as_view({'get': 'list'}), name='leaderboard'),
]
