from django.urls import path
from .views import AgentRequestLoanView, ApproveOrRejectLoanView, EditLoanView, ListAdminAgentLoanView, \
                   ListCustomerLoanView

urlpatterns = [
    path('customer-loan/', AgentRequestLoanView.as_view(), name='customer-loan'),
    path('approve-reject-loan/<int:pk>/', ApproveOrRejectLoanView.as_view(), name='approve-reject-loan'),
    path('edit-loan/<int:pk>/', EditLoanView.as_view(), name='edit-loan'),
    path('list-loans-admin-agent/', ListAdminAgentLoanView.as_view(), name='list-loans-admin-agent'),
    path('list-loans-customer/', ListCustomerLoanView.as_view(), name='list-loans-customer'),

]
