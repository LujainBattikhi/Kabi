from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from Kabi.apps.accounts.views import SignupView, CustomLoginView, logout_view
from Kabi.apps.jobs.views import HomePageView

app_name = 'jobs'
urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
]