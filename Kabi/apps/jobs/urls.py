from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from Kabi.apps.accounts.views import SignupView, CustomLoginView, logout_view

app_name = 'jobs'
urlpatterns = [
]