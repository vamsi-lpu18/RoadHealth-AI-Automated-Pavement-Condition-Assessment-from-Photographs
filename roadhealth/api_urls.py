"""
API URL configuration for RoadHealth AI
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App APIs
    path('accounts/', include('accounts.api_urls')),
    path('core/', include('core.api_urls')),
    path('analysis/', include('analysis.api_urls')),
]
