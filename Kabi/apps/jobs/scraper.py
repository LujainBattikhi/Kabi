import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/path/to/chromedriver"

# Glassdoor URL
GLASSDOOR_URL = "https://www.glassdoor.com"


# Login to Glassdoor via Google
def login_to_glassdoor(driver):
    """Log in to Glassdoor using Google Sign-In."""
    try:
        # Navigate to Glassdoor login page
        driver.get("https://www.glassdoor.com/profile/login_input.htm")

        # Click the "Continue with Google" button
        google_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='googleBtn']"))
        )
        google_button.click()

        # Switch to Google login popup
        driver.switch_to.window(driver.window_handles[1])

        # Enter Google email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys("battikhistays@gmail.com")  # Replace with your email
        email_input.send_keys(Keys.RETURN)

        # Wait for password field to load
        time.sleep(2)

        # Enter Google password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys("Battikhi@001")  # Replace with your password
        password_input.send_keys(Keys.RETURN)

        # Wait for login to complete
        time.sleep(5)

        # Switch back to the main Glassdoor window
        driver.switch_to.window(driver.window_handles[0])
        print("Successfully logged in to Glassdoor.")
    except Exception as e:
        print("Error during login:", str(e))
        driver.quit()


def start_driver():
    """Initialize Selenium WebDriver for headless Chrome in Docker."""
    options = Options()
    options.add_argument("start-maximized")  # Start browser maximized
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    options.binary_location = "/usr/bin/chromium"  # Chrome binary location in Docker
    options.add_argument("--headless")  # Run in headless mode for Docker
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues

    service = Service('/usr/bin/chromedriver')  # Chromedriver location in Docker
    driver = webdriver.Chrome(service=service, options=options)
    # login_to_glassdoor(driver)
    return driver


def scrape_jobs():
    """Scrape job listings from Glassdoor."""
    from Kabi.apps.jobs.models import JobPosting
    try:
        driver = start_driver()
        # Navigate to job search page
        driver.get(
            "https://www.glassdoor.com/Job/new-york-state-us-python-developer-jobs-SRCH_IL.0,17_IS428_KO18,34.htm"
        )
        # Wait for the job listings to load
        time.sleep(5)

        # Scrape job data
        jobs = []
        job_cards = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")  # Replace with actual class name

        for job_card in job_cards:
            try:
                title = job_card.find_element(
                    By.CLASS_NAME,
                    "JobCard_jobTitle__GLyJ1"
                ).text  # Replace with actual selector
                company = job_card.find_element(
                    By.CLASS_NAME,
                    "EmployerProfile_compactEmployerName__9MGcV"
                ).text  # Replace
                location = job_card.find_element(
                    By.CLASS_NAME, "JobCard_location__Ds1fM"
                ).text  # Replace
                salary = job_card.find_element(
                    By.CLASS_NAME, "JobCard_salaryEstimate__QpbTW"
                ).text  # Replace
                description = job_card.find_element(
                    By.CLASS_NAME,
                    "JobCard_jobDescriptionSnippet__l1tnl"
                ).text  # Replace
                jobs.append(
                    JobPosting(
                        title=title,
                        company_name=company,
                        location=location,
                        salary=salary,
                        description=description,
                    )
                )
            except:
                continue
        print(f"Scraped {len(jobs)} jobs.")
        return jobs
    except Exception as e:
        print("Error during scraping:", str(e))
        driver.quit()
