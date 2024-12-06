from celery import shared_task

from Kabi.apps.jobs.scraper import scrape_jobs


@shared_task
def health_checker():
    print("Celery Beat is working!")

@shared_task
def load_jobs():
    scrape_jobs()
