from django.urls import reverse, resolve
from django.test import  SimpleTestCase
from loan.views import AgentRequestLoanView, ApproveOrRejectLoanView, EditLoanView, ListAdminAgentLoanView, \
                        ListCustomerLoanView


class TestURLs(SimpleTestCase):

    def test_loan_request(self):
        url = reverse('customer-loan')
        self.assertEqual(resolve(url).func.view_class, AgentRequestLoanView)

    def test_approve_or_reject_loan(self):
        url = reverse('approve-reject-loan', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ApproveOrRejectLoanView)

    def test_edit_loan(self):
        url = reverse('edit-loan', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, EditLoanView)

    def test_list_loan_admin_agent(self):
        url = reverse('list-loans-admin-agent')
        self.assertEqual(resolve(url).func.view_class, ListAdminAgentLoanView)

    def test_list_loans_customer(self):
        url = reverse('list-loans-customer')
        self.assertEqual(resolve(url).func.view_class, ListCustomerLoanView)
