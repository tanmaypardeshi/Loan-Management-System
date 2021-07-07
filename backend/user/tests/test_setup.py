from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

from user.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignupTestSetUp(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.customer_data = {
            "email": "customer@gmail.com",
            "password": "django1234",
            "first_name": "Customer",
            "last_name": "0",
            "is_customer": True,
            "is_agent": False
        }
        self.agent_data = {
            "email": "agent@gmail.com",
            "password": "django1234",
            "first_name": "Agent",
            "last_name": "0",
            "is_customer": False,
            "is_agent": True
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class CreateAdminTestSetup(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="temp@gmail.com", password="django1234")
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.admin_url = reverse('create-admin')
        self.admin_data = {
            "email": "admin@gmail.com",
            "password": "django1234",
            "first_name": "Admin",
            "last_name": "0"
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class LoginTestSetup(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.login = {
            "email": "temp@gmail.com",
            "password": "django1234",
        }
        self.incorrect_email_login = {
            "email": "incorrect@gmail.com",
            "password": "django1234"
        }

        self.incorrect_password_login = {
            "email": "temp@gmail.com",
            "password": "dango1234",
        }

        self.incorrect_login = {
            "email": "temp@gmil.com",
            "password": "django123",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ProfileTestSetUp(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="temp@gmail.com", password="django1234")
        self.user.first_name = "dummy"
        self.user.last_name = "dummy"
        self.user.is_customer = True
        self.user.is_agent = False
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.profile_url = reverse('profile')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ListAgentTestSetup(APITestCase):
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

        agent_data = {
            "email": "agent@gmail.com",
            "password": "django1234",
            "first_name": "Agent",
            "last_name": "0",
            "is_customer": False,
            "is_agent": True
        }
        self.url = reverse('list-agent')
        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        self.agent = User.objects.create_user(email=agent_data['email'], password=agent_data['password'],
                                              is_customer=agent_data['is_customer'],
                                              is_agent=agent_data['is_agent'], is_approved=True)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ListAdminTestSetup(APITestCase):
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

        self.url = reverse('list-admin')
        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ListApprovalsTestSetup(APITestCase):
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

        self.url = reverse('list-approvals')
        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class ApproveDeleteTestSetup(APITestCase):
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
        agent = User.objects.create_user(email="temp@gmail.com", password="temp_pass", is_customer=False, is_agent=True)
        self.url = reverse('approve-delete', kwargs={'pk': agent.pk})
        self.admin = User.objects.create_superuser(email=admin_data['email'], password=admin_data['password'])
        self.customer = User.objects.create_user(email=customer_data['email'], password=customer_data['password'],
                                                 is_customer=customer_data['is_customer'],
                                                 is_agent=customer_data['is_agent'])
        return super().setUp()

    def tearDown(self):
        return super().tearDown()