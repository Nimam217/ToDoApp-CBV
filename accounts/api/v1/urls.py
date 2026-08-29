from django.contrib.auth.management.commands import changepassword
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
TokenVerifyView,
)

from .views import (
    CustomAuthToken,
    CustomDiscardAuthToken,
    RegistrationApiView,
    ProfileApiView,
    CustomObtainPairView, ChangePasswordView, ActivationView, ResendActivationEmail,
ResetPasswordView,ResetPasswordEmailView,
)

app_name = 'accounts-api-v1'

urlpatterns = [

    #Register
    path(
        'registration/',
        RegistrationApiView.as_view(),
        name='registration'
    ),
    # Token auth
    path(
        'token-auth/create/',
        CustomAuthToken.as_view(),
         name='token_auth'),
    path(
        'token-auth/discard/',
        CustomDiscardAuthToken.as_view(),
        name='discard_auth_token'
    ),
    # Profile
    path(
        'profile/',
        ProfileApiView.as_view(),
        name='profile'

    ),

    # Jwt Auth
    path(
        'jwt/create/'
        , CustomObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'jwt/refresh/',
         TokenRefreshView.as_view(),
        name='token_refresh'),

    path(
        'jwt/verify/'
        , TokenVerifyView.as_view()
        , name='token_verify'
    ),

    # Change Password
    path(
        'change_password/',
        ChangePasswordView.as_view(),
        name='change_password'

    ),
    # Reset Password

    path(
        'reset_password/',
        ResetPasswordEmailView.as_view(),
        name='reset_password'

    ),
    path(
        'reset_password/confirm/<str:token>/',
        ResetPasswordView.as_view(),
        name='reset_password'

    ),

    # Activation
    path(
        'activation/resend/',
        ResendActivationEmail.as_view(),
        name="activation_resend"
    ),
    path(
        'activation/confirm/<str:token>/',
            ActivationView.as_view(),
        name="activation"
    ),


 ]
