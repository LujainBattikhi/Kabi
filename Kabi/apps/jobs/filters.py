from .models import JobPosting
from django.db.models import Q
import django_filters

class JobPostingFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter', label="Search")

    class Meta:
        model = JobPosting
        fields = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(location__icontains=value)
        )