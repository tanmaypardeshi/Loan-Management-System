from django.urls import reverse, resolve
from django.test import  SimpleTestCase
from user.views import UserView, CreateAdminView, LoginView, ProfileView, ListAdminUserView, ListAgentUserView, \
                        ListApprovalsView, ApproveDeleteAgentView


class TestURLs(SimpleTestCase):

    def test_signup(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, UserView)

    def test_create_admin(self):
        url = reverse('create-admin')
        self.assertEqual(resolve(url).func.view_class, CreateAdminView)

    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_view_profile(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_list_agent(self):
        url = reverse('list-agent')
        self.assertEqual(resolve(url).func.view_class, ListAgentUserView)

    def test_list_admin(self):
        url = reverse('list-admin')
        self.assertEqual(resolve(url).func.view_class, ListAdminUserView)

    def test_list_approvals(self):
        url = reverse('list-approvals')
        self.assertEqual(resolve(url).func.view_class, ListApprovalsView)

    def test_approve_delete_agent(self):
        url = reverse('approve-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ApproveDeleteAgentView)

