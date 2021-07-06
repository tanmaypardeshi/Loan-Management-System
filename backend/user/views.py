import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import ValidationError

from .permissions import (IsAdmin, IsAgent, IsCustomer)
from .models import (User, )
from .serializers import (UserSerializer, LoginSerializer, )

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            response = {
                'success': False,
                'messge': 'This account already exists',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        user = User.objects.get(email=request.data['email'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = {
            'success': True,
            'message': 'User registered successfully',
            'token': token
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            response = {
                'success': True,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'is_customer': serializer.data['is_customer'],
                'is_agent': serializer.data['is_agent'],
                'is_admin': serializer.data['is_admin']
            }
            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            response = {
                'success': False,
                'message': f'Internal Server Error. Error : {e.__dict__["detail"]["non_field_errors"][0]}'
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(email=request.user)
            last_login = str(user.last_login + datetime.timedelta(hours=5.5))
            date_joined = str(user.date_joined + datetime.timedelta(hours=5.5))
            last_login = f"{last_login[:10]} {last_login[11:19]}"
            date_joined = f"{date_joined[:10]} {date_joined[11:19]}"
            response = {
                'success': True,
                'message': 'Profile fetched',
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_customer': user.is_customer,
                'is_agent': user.is_agent,
                'is_admin': user.is_admin,
                'last_login': last_login,
                'date_joined': date_joined
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': 'User does not exists',
                'error': str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
