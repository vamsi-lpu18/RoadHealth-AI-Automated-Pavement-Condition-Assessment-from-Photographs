from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_image, name='upload_image'),
    path('images/', views.image_list, name='image_list'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),
    path('map/', views.map_view, name='map_view'),
]
