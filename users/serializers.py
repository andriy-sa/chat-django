from django.contrib.auth import authenticate
from rest_framework.serializers import (
    CharField, ChoiceField, IntegerField, ModelSerializer, Serializer, ValidationError)

from andy_app import constants

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'country', 'city', 'gender', 'created_at', 'last_login']


class UsersListReqSerializer(Serializer):
    q = CharField(required=False, allow_blank=True)
    country = CharField(required=False, allow_null=True)
    gender = ChoiceField(required=False, choices=constants.GENDER_TYPES, allow_null=True)
    page = IntegerField(min_value=1)
    limit = IntegerField(min_value=1, max_value=1000)


class UserCreateSerializer(ModelSerializer):
    gender = ChoiceField(choices=constants.GENDER_TYPES)
    password = CharField()
    password_confirm = CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'country', 'city', 'gender', 'password', 'password_confirm']

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise ValidationError("Password Confirm not match password field.")

        return value


class LoginSerializer(Serializer):
    email = CharField(max_length=255)
    username = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError({'credentials': 'A user with this email and password was not found.'})

        if not user.is_active:
            raise ValidationError({'credentials': 'This user has been deactivated.'})

        self.context['user'] = user

        return data
