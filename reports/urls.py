from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:pk>/', views.generate_report, name='generate_report'),
    path('preview/<int:pk>/', views.report_preview, name='report_preview'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('summary/', views.summary_report, name='summary_report'),
]
