from django.urls import path
from .views import CustomerRequestLoanView, ApproveOrRejectLoanView

urlpatterns = [
    path('customer-loan/', CustomerRequestLoanView.as_view(), name='customer-loan'),
    path('approve-reject-loan/<int:pk>/', ApproveOrRejectLoanView.as_view(), name='approve-reject-loan'),
]
