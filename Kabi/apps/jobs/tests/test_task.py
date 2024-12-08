# Kabi/apps/jobs/tests/test_tasks.py
from django.test import TestCase
from django.conf import settings
from unittest.mock import patch
from Kabi.apps.jobs.models import JobPosting
from Kabi.apps.jobs.tasks import load_jobs

class TestLoadJobsTask(TestCase):
    @patch('Kabi.apps.jobs.tasks.scrape_jobs')
    def test_load_jobs_creates_new_jobs(self, mock_scrape_jobs):
        """
        Test that load_jobs creates new jobs from scraped data
        :param mock_scrape_jobs:
        :return:
        """
        mock_scrape_jobs.return_value = [
            {
                "title": "Senior Python Developer",
                "company_name": "TechCorp",
                "location": "New York, NY",
                "salary": "$120,000",
                "description": "Senior Python developer role..."
            },
            {
                "title": "Junior Python Developer",
                "company_name": "DevStartup",
                "location": "San Francisco, CA",
                "salary": "$90,000",
                "description": "Junior Python developer role..."
            }
        ]

        load_jobs()

        self.assertEqual(JobPosting.objects.count(), 2)
        job1 = JobPosting.objects.get(title="Senior Python Developer")
        self.assertEqual(job1.company_name, "TechCorp")
        self.assertEqual(job1.location, "New York, NY")

    @patch('Kabi.apps.jobs.tasks.scrape_jobs')
    def test_load_jobs_updates_existing_jobs(self, mock_scrape_jobs):
        """
        Test that load_jobs updates existing jobs with new data
        :param mock_scrape_jobs:
        :return:
        """
        existing_job = JobPosting.objects.create(
            title="Senior Python Developer",
            company_name="TechCorp",
            location="New York, NY",
            salary="$110,000",
            description="Old description"
        )

        mock_scrape_jobs.return_value = [
            {
                "title": "Senior Python Developer",
                "company_name": "TechCorp",
                "location": "New York, NY",
                "salary": "$130,000",
                "description": "Updated role description..."
            }
        ]

        load_jobs()

        existing_job.refresh_from_db()
        self.assertEqual(existing_job.salary, "$130,000")
        self.assertEqual(existing_job.description, "Updated role description...")
