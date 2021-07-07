import datetime

from django.http import Http404
from django.utils import timezone

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from user.permissions import IsAdmin, IsAgent, IsCustomer, IsAdminOrAgent
from user.models import User

from .models import Loan
from .serializers import AgentRequestSerializer, ApproveOrRejectLoanSerializer, EditLoanSerializer, ListLoanSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def calculate_interest(principal):
    if 10000 <= principal < 1000000:
        return 8.45
    elif 1000000 <= principal < 2500000:
        return 10
    else:
        return 12


def calculate_emi(principal, months, rate):
    rate_per_month = float(rate) / 1200
    numerator = float((1 + rate_per_month) ** months)
    denominator = numerator - 1
    return principal * rate_per_month * (numerator / denominator)


class AgentRequestLoanView(APIView):
    permission_classes = (IsAuthenticated, IsAgent,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        try:
            data = dict()
            granted_by = User.objects.get(email=request.user)
            user = User.objects.get(email=request.data['user'])
            data['user'] = user.pk
            data['granted_by'] = granted_by.pk
            data['principal'] = request.data['principal']
            data['interest'] = calculate_interest(request.data['principal'])
            data['months'] = request.data['months']
            data['emi'] = calculate_emi(request.data['principal'], request.data['months'], data['interest'])
            data['amount'] = data['emi'] * request.data['months']
            data['status'] = "NEW"
            data['start_date'] = timezone.localtime()
            data['end_date'] = timezone.localtime() + datetime.timedelta(hours=request.data['months'] * 730)
            serializer = AgentRequestSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                "success": True,
                "message": "Request for a loan has been submitted. Out agent will review and approve/reject the loan."
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': f'Internal Server Error. Error : {e}'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ApproveOrRejectLoanView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def put(self, request, pk):
        try:
            message = ""
            instance = self.get_object(pk)
            serializer = ApproveOrRejectLoanSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                if request.data['status'] == "APPROVED":
                    message = f"Loan id {pk} has been approved"
                elif request.data['status'] == "REJECTED":
                    message = f"Loan id {pk} has been rejected"
                response = {
                    "success": True,
                    "message": message
                }
                return Response(response, status=status.HTTP_200_OK)
            response = {
                "success": False,
                "message": "Could Not Approve or Reject Loan"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "success": False,
                "message": "Could Not Approve Or Reject Loan"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EditLoanView(APIView):
    permission_classes = (IsAuthenticated, IsAgent,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self, pk):
        try:
            return Loan.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404

    def put(self, request, pk):
        try:
            instance = self.get_object(pk)
            if instance.status == "APPROVED":
                response = {
                    'success': False,
                    'message': 'Cannot Edit Approved Loan'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            data = dict()
            data['principal'] = request.data['principal']
            data['interest'] = calculate_interest(request.data['principal'])
            data['months'] = request.data['months']
            data['emi'] = calculate_emi(request.data['principal'], request.data['months'], data['interest'])
            data['amount'] = data['emi'] * request.data['months']
            data['status'] = "NEW"
            data['start_date'] = timezone.localtime()
            data['end_date'] = timezone.localtime() + datetime.timedelta(hours=request.data['months'] * 730)
            serializer = EditLoanSerializer(instance, data=data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "success": True,
                    "message": "Edited Loan Detail Successfully"
                }
                return Response(response, status=status.HTTP_200_OK)
            response = {
                "success": False,
                "message": "Could Not Edit Loan"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "success": False,
                "message": "Could Not Edit Loan"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ListAdminAgentLoanView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminOrAgent,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListLoanSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        qs = Loan.objects.all()
        if status is not None:
            qs = qs.filter(status=status)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ListCustomerLoanView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsCustomer,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ListLoanSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status')
        qs = Loan.objects.filter(user=self.request.user)
        if status is not None:
            qs = qs.filter(status=status)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
