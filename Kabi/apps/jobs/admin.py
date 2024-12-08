from django.contrib import admin, messages
from .models import JobPosting

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'salary', 'date_posted')
    list_filter = ('company_name', 'location', 'date_posted')
    search_fields = ('title', 'company_name', 'description')
    ordering = ('-date_posted',)


    actions = ['trigger_load_jobs']

    @admin.action(description="Load Jobs via Celery")
    def trigger_load_jobs(self, request, queryset):
        from Kabi.apps.jobs.tasks import load_jobs
        load_jobs()
        self.message_user(request, "Job loading task has been triggered successfully!", messages.SUCCESS)
