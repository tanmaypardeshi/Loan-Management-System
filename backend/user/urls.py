from django.urls import path
from .views import UserView, LoginView, ProfileView

urlpatterns = [
    path('signup/', UserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile')
]
