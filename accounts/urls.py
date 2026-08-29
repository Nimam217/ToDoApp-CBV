from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordResetDoneView

from .views import (
    RegisterView,
    LogoutConfirmView,
    CustomPasswordResetView,
    CustomLoginView, CustomPasswordResetConfirmView, ProfileView,
    ProfileUpdateView,
    PasswordChangeConfirmView, PasswordChangeView
)

app_name = "accounts"

urlpatterns = [

    # Custom Login
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),

    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    # Custom Password Reset
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),

    # Password Reset Done
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(),
        name="password_change",

    ),
    path(
        "password_change/done/",
         PasswordChangeConfirmView.as_view(),
         name="password_change_done"),
    # Django Auth URLs
    path(
        "",
        include("django.contrib.auth.urls"),
    ),

    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Logout confirmation
    path(
        "logout_confirm/",
        LogoutConfirmView.as_view(),
        name="logout_confirm",
    ),
    path(
        "profile/<int:pk>/",
        ProfileView.as_view(),
        name="profile",
    ),
path(
    "profile/<int:pk>/edit/",
    ProfileUpdateView.as_view(),
    name="profile_edit",
),


    path(
        'api/v1/',
        include('accounts.api.v1.urls',namespace="accounts-api-v1")
    ),
]