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
def login_via_google(driver):
    print("Logging in via Google...")
    driver.get(GLASSDOOR_URL)
    time.sleep(5)  # Wait for page to load

    # Click "Sign in with Google" button
    try:
        google_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in with Google')]")
        google_button.click()
        time.sleep(3)
    except Exception as e:
        print("Failed to find Google login button:", e)

    # Switch to Google login window
    driver.switch_to.window(driver.window_handles[-1])

    # Enter Google credentials
    email_input = driver.find_element(By.XPATH, "//input[@type='email']")
    email_input.send_keys("battikhistays@gmail.com")  # Replace with your email
    email_input.send_keys(Keys.RETURN)
    time.sleep(2)

    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys("Battikhi@001")  # Replace with your password
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Switch back to Glassdoor
    driver.switch_to.window(driver.window_handles[0])
    print("Logged in successfully!")
def start_driver():
    """Initialize Selenium WebDriver for headless Chrome in Docker."""
    options = Options()
    options.add_argument("start-maximized")  # Start browser maximized
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    options.binary_location = "/usr/bin/chromium"  # Chrome binary location in Docker

    service = Service('/usr/bin/chromedriver')  # Chromedriver location in Docker
    driver = webdriver.Chrome(service=service, options=options)
    login_via_google(driver)
    return driver


def scrape_glassdoor_jobs():
    """Scrape job postings from Glassdoor."""
    url = "https://www.glassdoor.com/Job/index.htm"  # Replace with your desired Glassdoor URL
    driver = start_driver()
    driver.get(url)

    try:
        # Wait until job listings are loaded
        wait = WebDriverWait(driver, 20)
        job_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.JobsList_jobListItem__wjTHv"))
        )

        jobs = []
        for job in job_elements:
            title = job.find_element(By.CSS_SELECTOR, ".jobTitle").text
            company = job.find_element(By.CSS_SELECTOR, ".jobEmpolyerName").text
            location = job.find_element(By.CSS_SELECTOR, ".loc").text
            jobs.append({"title": title, "company": company, "location": location})

        return jobs
    finally:
        driver.quit()
