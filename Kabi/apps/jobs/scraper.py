import requests
from bs4 import BeautifulSoup
from Kabi.apps.jobs.models import JobPosting

def scrape_glassdoor():
    url = "https://www.glassdoor.com/Job/jobs.htm"  # Replace with the target Glassdoor URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Glassdoor. Status Code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    job_elements = soup.find_all('div', class_='job')  # Update with actual class/selector for job listings

    for job_element in job_elements:
        job_title = job_element.find('a', class_='job-title').text.strip()
        company_name = job_element.find('div', class_='company-name').text.strip()
        location = job_element.find('span', class_='location').text.strip()
        job_description = job_element.find('div', class_='job-snippet').text.strip()

        # Save to database if not already present
        JobPosting.objects.get_or_create(
            job_title=job_title,
            company_name=company_name,
            location=location,
            defaults={'job_description': job_description}
        )
