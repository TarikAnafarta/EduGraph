# -*- coding: utf-8 -*-
"""
Main URL configuration for EduGraph backend.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.users.views import login_view, register_view, verify_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.artifacts.urls')),
    path('api/users/', include('backend.users.urls')),
    # Template URLs
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify/', verify_view, name='verify'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', dashboard_view, name='home'),  # Redirect root to dashboard
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)
