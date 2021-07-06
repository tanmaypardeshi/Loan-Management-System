from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Loan


def validate_principal(value):
    if value < 10000:
        raise ValidationError('Principal Amount Cannot be less than 10000')


class AgentRequestSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ['user', 'granted_by', 'principal', 'interest', 'months', 'emi', 'amount', 'status', 'start_date',
                  'end_date']


class ListLoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class ApproveOrRejectLoanSerializer(Serializer):
    status = serializers.CharField(max_length=12)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class EditLoanSerializer(Serializer):
    principal = serializers.FloatField(default=10000, validators=[validate_principal])
    interest = serializers.FloatField(default=9)
    months = serializers.IntegerField(default=0)
    amount = serializers.FloatField(default=0)
    emi = serializers.FloatField(default=0)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def update(self, instance, validated_data):
        instance.principal = validated_data.get('principal', instance.principal)
        instance.interest = validated_data.get('interest', instance.interest)
        instance.months = validated_data.get('months', instance.months)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.emi = validated_data.get('emi', instance.emi)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance