from django.test import TestCase
from Kabi.apps.jobs.scraper import scrape_jobs

class TestScraper(TestCase):
    def test_scrape_jobs_returns_valid_data(self):
        data = scrape_jobs()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Check the structure of the first job dict
        first_job = data[0]
        self.assertIn('title', first_job)
        self.assertIn('company_name', first_job)
        self.assertIn('location', first_job)
        self.assertIn('salary', first_job)
        self.assertIn('description', first_job)
