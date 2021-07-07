from django.urls import path
from .views import UserView, LoginView, ProfileView, ListAdminUserView, ListAgentUserView, CreateAdminView, \
                    ListApprovalsView, ApproveDeleteAgentView

urlpatterns = [
    path('signup/', UserView.as_view(), name='signup'),
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list-agent/', ListAgentUserView.as_view(), name='list-agent'),
    path('list-admin/', ListAdminUserView.as_view(), name='list-admin'),
    path('list-approvals/', ListApprovalsView.as_view(), name='list-approvals'),
    path('approve-delete/<int:pk>/', ApproveDeleteAgentView.as_view(), name='approve-delete')
]
