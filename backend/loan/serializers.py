from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_jwt.settings import api_settings

from user.models import User
from .models import Loan


class CustomerRequestSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ['user', 'granted_by', 'principal', 'interest', 'months', 'emi', 'amount', 'status', 'start_date',
                  'end_date']


class ApproveOrRejectLoanSerializer(Serializer):
    status = serializers.CharField(max_length=12)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance