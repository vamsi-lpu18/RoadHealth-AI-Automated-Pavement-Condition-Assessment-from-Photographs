from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.UserRegistrationAPIView.as_view(), name='api_register'),
    path('profile/', api_views.UserProfileAPIView.as_view(), name='api_profile'),
    path('change-password/', api_views.change_password, name='api_change_password'),
    path('stats/', api_views.user_stats, name='api_user_stats'),
]
