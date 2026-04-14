from django.urls import path
from .views import register, login, profile, check_email, reset_password

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("profile/", profile),
    path("check-email/", check_email),
    path("reset-password/", reset_password),
]
