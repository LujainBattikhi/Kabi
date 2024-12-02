from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from Kabi.apps.accounts.views import SignupView, CustomLoginView, logout_view

app_name = 'accounts'
urlpatterns = [
    path('sign-up/', SignupView.as_view(), name='sign_up'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]