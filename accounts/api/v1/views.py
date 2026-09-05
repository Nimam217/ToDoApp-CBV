from django.conf import settings
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

import jwt

from ...models import Profile, User
from .permissions import IsVerifiedUser
from .serializers import (
    AuthTokenSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    RegisterSerializer,
    ResendActivationSerializer,
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
    TokenObtainPairViewSerializer,
)
from accounts.services import (
    send_activation_email,
    send_reset_password_email,
)


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        send_activation_email(user, token)

        return Response(
            {
                "email": user.email,
                "detail": "Check your email box",
            },
            status=status.HTTP_201_CREATED,
        )


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsVerifiedUser,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairViewSerializer


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": ["wrong password"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password1"])
        user.save()

        return Response(
            {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        send_reset_password_email(user, token)

        return Response(
            {"email": "Successfully send"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            user = User.objects.get(pk=decoded_token["user_id"])

            if not user.is_verified:
                raise AuthenticationFailed("User is not verified")

            serializer.is_valid(raise_exception=True)

            user.set_password(serializer.validated_data["new_password1"])
            user.save()

            return Response(
                {"password": "Successfully reset your password"},
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activations link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid Token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ActivationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            user = User.objects.get(pk=decoded_token["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()

                return Response(
                    {"email": "Successfully activated"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "User has already been verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activations link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid Token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendActivationEmail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResendActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        send_activation_email(user, token)

        return Response(
            {"detail": "email has been sent successfully"},
            status=status.HTTP_200_OK,
        )
