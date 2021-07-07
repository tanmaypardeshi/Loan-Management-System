import datetime

from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import ValidationError

from .permissions import IsAdmin, IsAgent, IsAdminOrAgent
from .models import User
from .serializers import UserSerializer, LoginSerializer, ListUserSerializer, CreateAdminSerializer, \
    ApproveAgentSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            response = {
                'success': False,
                'message': 'This account already exists',
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


class CreateAdminView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        user_serializer = CreateAdminSerializer(data=request.data)
        if not user_serializer.is_valid():
            response = {
                'success': False,
                'message': 'This account already exists',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'success': True,
            'message': 'Admin registered successfully',
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
                'message': f'Internal Server Error'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(email=request.user)
            response = {
                'success': True,
                'message': 'Profile fetched',
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_customer': user.is_customer,
                'is_agent': user.is_agent,
                'is_admin': user.is_admin,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': 'User does not exists',
                'error': str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ListAgentUserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrAgent,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListUserSerializer
    queryset = User.objects.filter(is_customer=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ListAdminUserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListUserSerializer
    queryset = User.objects.filter(Q(is_customer=True) | Q(is_agent=True))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ListApprovalsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListUserSerializer
    queryset = User.objects.filter(is_agent=True, is_approved=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ApproveDeleteAgentView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = ApproveAgentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "message": f"Agent id {pk} has been approved"
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "success": False,
            "message": "Could not approve agent"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        try:
            instance.delete()
            response = {
                "success": True,
                "message": f"Agent id {pk} has been deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                "success": False,
                "message": "Could not delete agent"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
