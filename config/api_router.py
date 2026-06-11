
from django.conf import settings
from django.views.static import serve
from django.urls import path, re_path

from route_planner.api.views import FuelRoutePlannerAPIView

# API URL patterns - Single comprehensive endpoint
urlpatterns = [
    # Single API endpoint for complete fuel route planning
    path('fuel-route/', FuelRoutePlannerAPIView.as_view(), name='fuel-route-planner'),
    
    # Static and media files
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]