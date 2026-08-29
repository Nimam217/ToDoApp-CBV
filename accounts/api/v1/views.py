from logging import raiseExceptions

from django.core.mail import message
from django.db.migrations import serializer
from django.db.models import Model
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .permissions import IsVerifiedUser
from .serializers import (AuthTokenSerializer, RegisterSerializer,
                          ProfileSerializer, ChangePasswordSerializer,
                          TokenObtainPairViewSerializer, ResendActivationSerializer
                          ,ResetPasswordSerializer,ResetPasswordEmailSerializer

                          )
from ...models import Profile, User
import jwt
from ToDoApp import settings
from .threads import EmailThread







class RegistrationApiView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email =serializer.validated_data['email']
        user = get_object_or_404(User,email=email)
        token = self.get_token_for_user(user)
        message = EmailMessage('email/activation_email.tpl', {'token': token , 'user':user},
                               "admin@gmail.com",
                               to=[email])

        EmailThread(message).start()
        data = {
            'email': email,
            'detail': "Check your email box",

        }
        return Response(data,status=status.HTTP_201_CREATED)


    def get_token_for_user(self, user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)




class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })



class CustomDiscardAuthToken(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request  , *args, **kwargs):
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
        serializer = self.serializer_class(data=request.data,)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': ['wrong password']}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password1'])
        user.save()

        return Response(
            {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer
    def post(self, request, *args, **kwargs):
        admin_gmail = "admin@gmail.com"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user)
        message = EmailMessage(template_name='email/reset_password_email.tpl',
            context={
            'token': token,
            'user':user
        },
            from_email=admin_gmail,
            to=[user.email]
                               )
        EmailThread(message).start()
        return Response({'email': 'Successfully send'}, status=status.HTTP_200_OK)

    def get_tokens_for_user(self,user):
        if not user.is_verified:
            raise AuthenticationFailed("User is not verified")
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self,request,token,*args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            decoded_token = jwt.decode(token,settings.SECRET_KEY ,algorithms=["HS256"])
            user = User.objects.get(pk=decoded_token['user_id'])
            if not user.is_verified:
                raise AuthenticationFailed("User is not verified")
            elif user.is_verified:

                serializer.is_valid(raise_exception=True)
                new_password1 = serializer.validated_data["new_password1"]
                user.set_password(new_password1)
                user.save()
                return Response(
                    {"password" : "Successfully reset your password"},
                    status=status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)



class ActivationView(APIView):

    def get(self,request,token,*args, **kwargs):

        try:
            decoded_token = jwt.decode(token,settings.SECRET_KEY ,algorithms=["HS256"])
            user = User.objects.get(pk=decoded_token['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            elif user.is_verified:
                return Response(
                    {"detail": "User has already been verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)



class ResendActivationEmail(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResendActivationSerializer
    def post(self,request,*args,**kwargs,):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = self.get_tokens_for_user(user)
        message = EmailMessage('email/activation_email.tpl', {'token': token,'user':user},
                               "admin@gmail.com",
                               [user.email])
        EmailThread(message).start()
        return Response({'detail':'email has been sent successfully'}, status=status.HTTP_200_OK)

    def get_tokens_for_user(self,user):
        if not user.is_verified:
            raise AuthenticationFailed("User is not verified")
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)