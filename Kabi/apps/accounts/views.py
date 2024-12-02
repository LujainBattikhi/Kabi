from braces.views import AnonymousRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import SignupForm


class SignupView(AnonymousRequiredMixin,FormView):
    template_name = 'accounts/sign_up.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')
    extra_context = {
        'body_class': 'center'
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CustomLoginView(AnonymousRequiredMixin, LoginView):
    template_name = 'accounts/login.html'
    authenticated_redirect_url = reverse_lazy('main:home_page')
    form_class = AuthenticationForm
    extra_context = {
        'body_class': 'center'
    }


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('accounts:login'))