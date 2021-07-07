from .test_setup import SignupTestSetUp, CreateAdminTestSetup, LoginTestSetup, ProfileTestSetUp, ListAgentTestSetup, \
                        ListApprovalsTestSetup, ApproveDeleteTestSetup
from rest_framework_jwt.settings import api_settings

from user.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignupTestViews(SignupTestSetUp):
    # If signup is tried without data
    def test_signup_with_no_data(self):
        response = self.client.post(self.signup_url)
        self.assertEqual(response.status_code, 400)

    # If customer signup is tried with correct data
    def test_signup_customer(self):
        response = self.client.post(self.signup_url, self.customer_data, format="json")
        self.assertEqual(response.status_code, 201)

    # If customer already exists
    def test_sign_up_customer_already_exists(self):
        user = User.objects.create_user(email=self.customer_data['email'], password=self.customer_data['password'])
        user.first_name = self.customer_data['first_name']
        user.last_name = self.customer_data['last_name']
        user.is_customer = self.customer_data['is_customer']
        user.is_agent = self.customer_data['is_agent']
        if user.is_agent:
            user.is_approved = False
        else:
            user.is_approved = True
        user.save()
        response = self.client.post(self.signup_url, self.customer_data, format="json")
        self.assertEqual(response.status_code, 400)

    # If customer signup is tried with correct data
    def test_signup_agent(self):
        response = self.client.post(self.signup_url, self.agent_data, format="json")
        self.assertEqual(response.status_code, 201)

    # If customer already exists
    def test_sign_up_agent_already_exists(self):
        user = User.objects.create_user(email=self.agent_data['email'], password=self.agent_data['password'])
        user.first_name = self.agent_data['first_name']
        user.last_name = self.agent_data['last_name']
        user.is_customer = self.agent_data['is_customer']
        user.is_agent = self.agent_data['is_agent']
        if user.is_agent:
            user.is_approved = False
        else:
            user.is_approved = True
        user.save()
        response = self.client.post(self.signup_url, self.agent_data, format="json")
        self.assertEqual(response.status_code, 400)


class CreateAdminTestViews(CreateAdminTestSetup):
    # If signup is tried without data
    def test_signup_with_no_data(self):
        response = self.client.post(self.admin_url)
        self.assertEqual(response.status_code, 400)

    # If admin already exists
    def test_create_admin_already_exists(self):
        user = User.objects.create_superuser(email=self.admin_data['email'], password=self.admin_data['password'])
        user.first_name = self.admin_data['first_name']
        user.last_name = self.admin_data['last_name']
        user.save()
        response = self.client.post(self.admin_url, self.admin_data, format="json")
        self.assertEqual(response.status_code, 400)

    # If admin signup is tried with correct data but with appropriate permission
    def test_admin_authenticated(self):
        response = self.client.post(self.admin_url, self.admin_data, format="json")
        self.assertEqual(response.status_code, 201)

    # If admin signup is tried with correct data but not by appropriate permission
    def test_admin_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.admin_url, self.admin_data, format="json")
        self.assertEqual(response.status_code, 401)


class LoginTestViews(LoginTestSetup):
    # If login is tried without data
    def test_login_with_no_data(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 400)

    # Successful login
    def test_login(self):
        user = User.objects.create_user(email=self.login['email'], password=self.login['password'])
        user.save()
        response = self.client.post(self.login_url, self.login, format="json")
        self.assertEqual(response.status_code, 200)

    # Incorrect password
    def test_login_incorrect_password(self):
        response = self.client.post(self.login_url, self.incorrect_password_login, format="json")
        self.assertEqual(response.status_code, 400)

    # Incorrect email
    def test_login_incorrect_email(self):
        response = self.client.post(self.login_url, self.incorrect_email_login, format="json")
        self.assertEqual(response.status_code, 400)

    # Incorrect credentials
    def test_login_incorrect(self):
        response = self.client.post(self.login_url, self.incorrect_login, format="json")
        self.assertEqual(response.status_code, 400)


class ProfileTestViews(ProfileTestSetUp):
    # Authenticated get request
    def test_admin_authenticated(self):
        response = self.client.get(self.profile_url, format="json")
        self.assertEqual(response.status_code, 200)

    # Unauthenticated get request
    def test_admin_not_authenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.profile_url, format="json")
        self.assertEqual(response.status_code, 401)


class ListAdminTestViews(ListAgentTestSetup):
    # Authenticated request by admin role
    def test_admin_authenticated(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Authenticated request by agent role
    def test_agent_authenticated(self):
        payload = jwt_payload_handler(self.agent)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by customer role - Will not work
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


class ListAgentTestViews(ListAdminTestViews):
    # Authenticated request by admin role
    def test_admin_authenticated(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Authenticated request by non admin role - Will not work
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


class ListApprovalsTestViews(ListApprovalsTestSetup):
    # Authenticated request by admin role
    def test_admin_authenticated(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # Authenticated request by non admin role - Will not work
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


class ApprovalDeleteTestViews(ApproveDeleteTestSetup):

    # Authenticated request by admin role to approve an agent
    def test_admin_authenticated_approve(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.put(self.url, {"is_approved": True}, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by admin role to delete an agent
    def test_admin_authenticated_delete(self):
        payload = jwt_payload_handler(self.admin)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, 200)

    # Authenticated request by non admin role - Will not work
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
