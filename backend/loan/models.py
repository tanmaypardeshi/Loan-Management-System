from django.db import models
from django.core.exceptions import ValidationError

from simple_history.models import HistoricalRecords

from user.models import User


def validate_principal(value):
    if value < 10000:
        raise ValidationError('Principal Amount Cannot be less than 10000')


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent', null=True, default=None)
    principal = models.FloatField(default=10000, validators=[validate_principal])
    interest = models.FloatField(default=9)
    months = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    emi = models.FloatField(default=0)
    status = models.CharField(max_length=12, default="NEW")
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.principal}"


