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
        if user.is_agent:
            user.is_approved = False
        else:
            user.is_approved = True
        user.save()
        return user


class CreateAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_superuser(email=validated_data['email'],
                                             password=validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.is_customer = False
        user.is_agent = False
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
        if not user.is_approved:
            raise serializers.ValidationError(
                'Agent login is not approved by admin'
            )
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        update_last_login(None, user)
        user_obj = {
            'email': user.email,
            'token': token,
            'is_customer': user.is_customer,
            'is_agent': user.is_agent,
            'is_admin': user.is_admin
        }
        return user_obj


class ListUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active']


class ApproveAgentSerializer(Serializer):
    is_approved = serializers.BooleanField(required=True)

    def update(self, instance, validated_data):
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance
