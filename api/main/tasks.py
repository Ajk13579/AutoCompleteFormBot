import datetime
import time

from celery import shared_task
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from .services import check_form_availability


def create_driver():
    """Create a driver with settings"""

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    return webdriver.Chrome(options=options)


def complete_form(browser, data: dict):
    """We sleep and fill out the form with data"""

    # First page
    inputs = browser.find_elements(By.CLASS_NAME, "b24-form-control")
    inputs[0].send_keys(data["username"])
    inputs[1].send_keys(data["lastname"])

    button = browser.find_element(By.CLASS_NAME, "b24-form-btn")
    button.click()

    # Loading the next page
    time.sleep(2)

    # Second page
    inputs = browser.find_elements(By.CLASS_NAME, "b24-form-control")
    inputs[0].send_keys(data["email"])
    inputs[1].send_keys(data["phone"])

    button = browser.find_elements(By.CLASS_NAME, "b24-form-btn")
    button[1].click()

    # Loading the next page
    time.sleep(2)

    # Third page
    inputs = browser.find_element(By.CLASS_NAME, "b24-form-control")
    inputs.send_keys(data["birthday"])

    button = browser.find_elements(By.CLASS_NAME, "b24-form-btn")
    button[1].click()


@shared_task
def fill_in_form_task(
        username: str,
        lastname: str,
        email: str,
        phone: str,
        birthday: str,
        user_id: str
) -> None:
    """
    Fills out a form on the website and
    takes a screenshot of the successful completion
    """

    if not check_form_availability():
        return None

    browser = create_driver()

    try:
        browser.get(settings.URL_FORM)
        # Loading a page
        time.sleep(5)

        data = {
            "username": username,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "birthday": birthday,
        }

        complete_form(browser, data)

        # Loading the ending screenshot of the page
        time.sleep(2)

        # Decide with what format we will create a screenshot
        if not settings.FORMAT_FOR_SAVING_FILE:
            formatted_date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        else:
            formatted_date_now = datetime.datetime.now().strftime(settings.FORMAT_FOR_SAVING_FILE)

        # Take screenshot
        browser.save_screenshot(f"screenshots/{formatted_date_now}_{user_id}.png")

    except Exception as _ex:
        # Catch errors and logging
        print(_ex)
    finally:
        # Close connection
        browser.close()
        browser.quit()
