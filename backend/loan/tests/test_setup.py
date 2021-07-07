import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from user.models import User
from loan.models import Loan

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


class AgentRequestLoanTestSetUp(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(email="cust@gmail.com", password="temp_pass", is_customer=True,
                                                 is_agent=False,
                                                 is_approved=True)
        self.agent = User.objects.create_user(email="temp@gmail.com", password="temp_pass", is_customer=False,
                                              is_agent=True,
                                              is_approved=True)
        self.not_approved = User.objects.create_user(email="temp1@gmail.com", password="temp_pass", is_customer=False,
                                                     is_agent=True,
                                                     is_approved=False)
        self.data = {
            "user": self.customer.email,
            "granted_by": self.agent.email,
            "principal": 1000000.00,
            "interest": calculate_interest(1000000.00),
            "months": 60,
            "emi": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)),
            "amount": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)) * 60,
            "status": "NEW",
            "start_date": timezone.localtime(),
            "end_date": timezone.localtime() + datetime.timedelta(hours=60 * 730)
        }
        payload = jwt_payload_handler(self.agent)
        token = jwt_encode_handler(payload)
        not_approved_payload = jwt_payload_handler(self.not_approved)
        self.not_approved_token = jwt_encode_handler(not_approved_payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.request_url = reverse('customer-loan')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ApproveOrRejectLoanTestSetup(APITestCase):
    def setUp(self):
        admin_data = {
            "email": "admin@gmail.com",
            "password": "django1234",
            "first_name": "Admin",
            "last_name": "0",
            "is_customer": False,
            "is_agent": False
        }

        customer_data = {
            "email": "customer@gmail.com",
            "password": "django1234",
            "first_name": "Customer",
            "last_name": "0",
            "is_customer": True,
            "is_agent": False
        }

        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.agent = User.objects.create_user(email="temp@gmail.com", password="temp_pass", is_customer=False,
                                              is_agent=True,
                                              is_approved=True)
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        data = {
            "user": self.customer,
            "granted_by": self.agent,
            "principal": 1000000.00,
            "interest": calculate_interest(1000000.00),
            "months": 60,
            "emi": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)),
            "amount": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)) * 60,
            "status": "NEW",
            "start_date": timezone.localtime(),
            "end_date": timezone.localtime() + datetime.timedelta(hours=60 * 730)
        }
        self.loan = Loan.objects.create(**data)
        self.request_url = reverse('approve-reject-loan', kwargs={'pk': self.loan.pk})
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class EditLoanTestSetUp(APITestCase):
    def setUp(self):
        customer_data = {
            "email": "customer@gmail.com",
            "password": "django1234",
            "first_name": "Customer",
            "last_name": "0",
            "is_customer": True,
            "is_agent": False
        }

        self.agent = User.objects.create_user(email="temp@gmail.com", password="temp_pass", is_customer=False,
                                              is_agent=True,
                                              is_approved=True)
        self.not_approved = User.objects.create_user(email="temp1@gmail.com", password="temp_pass", is_customer=False,
                                                     is_agent=True,
                                                     is_approved=False)
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        payload = jwt_payload_handler(self.agent)
        token = jwt_encode_handler(payload)
        not_approved_payload = jwt_payload_handler(self.not_approved)
        self.not_approved_token = jwt_encode_handler(not_approved_payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data1 = {
            "user": self.customer,
            "granted_by": self.agent,
            "principal": 1000000.00,
            "interest": calculate_interest(1000000.00),
            "months": 60,
            "emi": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)),
            "amount": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)) * 60,
            "status": "NEW",
            "start_date": timezone.localtime(),
            "end_date": timezone.localtime() + datetime.timedelta(hours=60 * 730)
        }

        data2 = {
            "user": self.customer,
            "granted_by": self.agent,
            "principal": 1000000.00,
            "interest": calculate_interest(1000000.00),
            "months": 60,
            "emi": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)),
            "amount": calculate_emi(1000000.00, 60, calculate_interest(1000000.00)) * 60,
            "status": "APPROVED",
            "start_date": timezone.localtime(),
            "end_date": timezone.localtime() + datetime.timedelta(hours=60 * 730)
        }

        self.edit_data = {
            "user": self.customer.email,
            "principal": 200000.00,
            "months": 60
        }
        self.loan1 = Loan.objects.create(**data1)
        self.loan2 = Loan.objects.create(**data2)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ListLoanAdminAgentTestSetUp(APITestCase):
    def setUp(self):
        admin_data = {
            "email": "admin@gmail.com",
            "password": "django1234",
            "first_name": "Admin",
            "last_name": "0",
            "is_customer": False,
            "is_agent": False
        }

        customer_data = {
            "email": "customer@gmail.com",
            "password": "django1234",
            "first_name": "Customer",
            "last_name": "0",
            "is_customer": True,
            "is_agent": False
        }

        self.url = reverse('list-loans-admin-agent')
        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ListLoansCustomerTestSetUp(APITestCase):
    def setUp(self):
        customer_data = {
            "email": "customer@gmail.com",
            "password": "django1234",
            "first_name": "Customer",
            "last_name": "0",
            "is_customer": True,
            "is_agent": False
        }

        self.url = reverse('list-loans-admin-agent')
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        return super().setUp()

    def tearDown(self):
        return super().tearDown()