"""
URL configuration for frecog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = "registration/password_reset_email.txt"  # Plain text fallback
    html_email_template_name = "registration/password_reset_email.html"  # HTML version


urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    # Include all URLs from the core app
    # This imports all routes defined in core/urls.py
    path("", include("core.urls")),
    # Include all URLs from the face app
    # This imports all routes defined in face/urls.py
    path("", include("face.urls")),
    # Django's built-in password management views
    # Password change functionality
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Password reset functionality (forgot password)
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Add static and media URL patterns for development
    # This allows Django to serve media files (including uploaded face images)
    # Note: In production, these should be served by a proper web server
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
