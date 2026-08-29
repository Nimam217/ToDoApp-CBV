from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True,max_length=200)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError(_('Passwords must match'))
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['image','email','first_name','last_name','description']


class TokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(_('Please verify your account.'))

        data["user"] = {
            'user_id': self.user.id,
            'email': self.user.email,

        }
        return data

class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

        def validate(self, attrs):
            password1 = attrs.get('new_password1')
            password2 = attrs.get('new_password2')
            if password1 != password2:
                raise serializers.ValidationError({'new_password1': _("The two password fields didn't match."),})
            try:
                validate_password(password1)

            except exceptions.ValidationError as e:
                raise serializers.ValidationError({'new_password1': list(e.messages)})

            return super().validate(attrs)


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, data):

        email = data.get('email')
        try:
            user = User.objects.get(email=email)


        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User does not exist'})

        data['user'] = user

        return super().validate(data)


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')
        if new_password1 != new_password2:
            raise serializers.ValidationError({'new_password1': _("The two password fields didn't match."),})
        try:
            validate_password(new_password1)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password1': list(e.messages)})

        return super().validate(data)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, data):
        data = super().validate(data)
        email = data.get('email')
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User does not exist'})
        data["user"] = user

        return data

