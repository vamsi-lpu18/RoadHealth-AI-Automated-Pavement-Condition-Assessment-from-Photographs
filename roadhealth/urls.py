"""
URL configuration for RoadHealth AI project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path('analysis/', include('analysis.urls')),
    path('reports/', include('reports.urls')),
    path('api/', include('roadhealth.api_urls')),
]

# Serve media and static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "RoadHealth AI Administration"
admin.site.site_title = "RoadHealth AI Admin Portal"
admin.site.index_title = "Welcome to RoadHealth AI Administration"
