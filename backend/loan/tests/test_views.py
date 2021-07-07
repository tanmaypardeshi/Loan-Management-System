from django.urls import reverse
from .test_setup import AgentRequestLoanTestSetUp, ApproveOrRejectLoanTestSetup, EditLoanTestSetUp, \
    ListLoanAdminAgentTestSetUp, ListLoansCustomerTestSetUp
from rest_framework_jwt.settings import api_settings

from user.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AgentRequestLoanTestViews(AgentRequestLoanTestSetUp):
    # If no data is sent
    def test_no_data_passed(self):
        response = self.client.post(self.request_url)
        self.assertEqual(response.status_code, 400)

    # If user is an agent and is approved
    def test_agent_approved_request(self):
        users = User.objects.all()
        response = self.client.post(self.request_url, self.data, format="json")
        self.assertEqual(response.status_code, 200)

    # If user is an agent is not approved
    def test_agent_not_approved_request(self):
        self.client.force_authenticate(user=self.not_approved, token=self.not_approved_token)
        response = self.client.post(self.request_url, self.data, format="json")
        self.assertEqual(response.status_code, 403)

    # If user is not authenticated
    def test_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.request_url, self.data, format="json")
        self.assertEqual(response.status_code, 401)


class ApproveOrRejectLoanTestViews(ApproveOrRejectLoanTestSetup):

    # If no data is sent
    def test_no_data_passed(self):
        response = self.client.post(self.request_url)
        self.assertEqual(response.status_code, 401)

    # Authenticated request by an admin role to accept loan
    def test_agent_approved_request(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.request_url, {'status': "APPROVED"}, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by an admin role to reject loan
    def test_agent_reject_loan_by_admin(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.request_url, {'status': "REJECTED"}, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by non admin role - Will not work
    def test_agent_approve_loan_by_admin(self):
        payload = jwt_payload_handler(self.customer)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.request_url, {'status': "APPROVED"}, format="json")
        self.assertEqual(response.status_code, 403)

    # If user is not authenticated
    def test_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(self.request_url, {'status': "ACCEPTED"}, format="json")
        self.assertEqual(response.status_code, 401)


class EditLoanTestViews(EditLoanTestSetUp):
    # If no data is sent
    def test_no_data_passed(self):
        response = self.client.put(reverse('edit-loan', kwargs={'pk': self.loan1.pk}), fornat="json")
        self.assertEqual(response.status_code, 400)

    # Authenticated request by an agent but agent is not approved yet
    def test_agent_fail_edit_loan(self):
        self.client.force_authenticate(user=self.not_approved, token=self.not_approved_token)
        response = self.client.put(reverse('edit-loan', kwargs={'pk': self.loan1.pk}), self.edit_data,
                                   format="json")
        self.assertEqual(response.status_code, 403)

    # Authenticated request by an agent who is approved
    def test_agent_success_edit_loan(self):
        response = self.client.put(reverse('edit-loan', kwargs={'pk': self.loan1.pk}), self.edit_data, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by an agent on an already approved loan
    def test_agent_fail_edit_loan_already_approved(self):
        response = self.client.put(reverse('edit-loan', kwargs={'pk': self.loan2.pk}), self.edit_data, format="json")
        self.assertEqual(response.status_code, 400)

    # If user is not authenticated
    def test_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(reverse('edit-loan', kwargs={'pk': self.loan1.pk}), self.edit_data, format="json")
        self.assertEqual(response.status_code, 401)


class ListLoansCustomerTestViews(ListLoansCustomerTestSetUp):

    # Authenticated request by customer
    def test_customer_authenticated(self):
        payload = jwt_payload_handler(self.customer)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 403)

    # Unauthenticated request
    def test_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 401)
