from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from Kabi.apps.jobs.scraper import  scrape_glassdoor_jobs


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # @todo this will be added in a celery task
        jobs = scrape_glassdoor_jobs()
        return context