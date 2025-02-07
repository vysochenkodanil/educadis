from django.urls import path, include
from .views import UserCreateView, UserProfileView, UserProfileUpdateView
from .views import AchievementListView, CoinListView

app_name = 'user'
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('edit_profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('achievements/', AchievementListView.as_view(), name='achievements'),
    path('coins/', CoinListView.as_view(), name='coins'),
]
