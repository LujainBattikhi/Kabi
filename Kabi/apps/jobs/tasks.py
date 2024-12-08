from celery import shared_task
from django.db import transaction

from Kabi.apps.jobs.scraper import scrape_jobs


@shared_task
def health_checker():
    print("Celery Beat is working!")

@shared_task
def load_jobs():
    scarped_jobs=scrape_jobs()
    handle_jobs_bulk_update_create(scarped_jobs)

def handle_jobs_bulk_update_create(scarped_jobs):
    from Kabi.apps.jobs.models import JobPosting

    existing = JobPosting.objects.values(
        'id', 'title', 'company_name', 'location'
    )
    existing_dict = {
        (item['title'], item['company_name'], item['location']): item['id']
        for item in existing
    }

    new_jobs = []
    updated_jobs = []

    for job_data in scarped_jobs:
        key = (job_data['title'], job_data['company_name'], job_data['location'])

        if key in existing_dict:
            updated_jobs.append(
                JobPosting(
                    id=existing_dict[key],
                    title=job_data['title'],
                    company_name=job_data['company_name'],
                    location=job_data['location'],
                    salary=job_data['salary'],
                    description=job_data['description']
                )
            )
        else:
            new_jobs.append(JobPosting(**job_data))

    with transaction.atomic():
        if new_jobs:
            JobPosting.objects.bulk_create(new_jobs)
            print(f"Created {len(new_jobs)} new jobs.")

        if updated_jobs:
            JobPosting.objects.bulk_update(updated_jobs, ['salary', 'description'])
            print(f"Updated {len(updated_jobs)} existing jobs.")
