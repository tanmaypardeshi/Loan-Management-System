from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_jwt.settings import api_settings
from .models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name',
                  'last_name', 'is_customer', 'is_agent']

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'],
                                        password=validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.is_customer = validated_data['is_customer']
        user.is_agent = validated_data['is_agent']
        user.is_admin = validated_data['is_admin']
        if user.is_agent:
            user.is_approved = False
        else:
            user.is_approved = True
        user.save()
        return user


class LoginSerializer(Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    is_admin = serializers.BooleanField(default=False)
    is_agent = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Invalid Credentials'
            )
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        update_last_login(None, user)
        return {
            'email': user.email,
            'token': token,
            'is_customer': user.is_customer,
            'is_agent': user.is_agent,
            'is_admin': user.is_admin
        }

