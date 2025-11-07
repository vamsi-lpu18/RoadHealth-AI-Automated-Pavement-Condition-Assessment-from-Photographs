from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'images', api_views.ImageRecordViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
]
