from django.db import models

class JobPosting(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job_title', 'company_name', 'location')

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
