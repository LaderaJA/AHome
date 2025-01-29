from django.urls import path
from .views import RegisterView, ProfileView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/',  ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]
