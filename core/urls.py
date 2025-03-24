from django.urls import path
from .views import (
    IndexView,
    UserLoginView,
    UserRegistrationView,
    UserLogoutView,
)

urlpatterns = [
    # Main application views
    # Homepage/dashboard for authenticated users
    path("", IndexView.as_view(), name="index"),
    # User authentication views
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    # Face management views (CRUD operations)
    # List all faces in the system
]
