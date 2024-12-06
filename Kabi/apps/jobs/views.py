from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from Kabi.apps.jobs.filters import JobPostingFilter
from Kabi.apps.jobs.models import JobPosting
from django_filters.views import FilterView


class HomePageView(LoginRequiredMixin, FilterView):
    template_name = 'jobs/home_page.html'
    model = JobPosting
    filterset_class = JobPostingFilter
    context_object_name = 'job_postings'
    paginate_by = 10
    def get_queryset(self):
        """Get the filtered queryset."""
        queryset = self.filterset_class(self.request.GET, queryset=self.model.objects.all()).qs
        return queryset

    def get_context_data(self, **kwargs):
        """Paginate the filtered queryset and pass it to the context."""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Pagination
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            paginated_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        context[self.context_object_name] = paginated_queryset
        context['paginator'] = paginator
        context['page_obj'] = paginated_queryset
        context['is_paginated'] = paginated_queryset.has_other_pages()
        return context