from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'main/home_page.html'

