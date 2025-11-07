from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'results', api_views.AnalysisResultViewSet, basename='analysis')

urlpatterns = [
    path('', include(router.urls)),
]
