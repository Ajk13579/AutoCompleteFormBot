import datetime
import time

from celery import shared_task
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@shared_task
def add(username, lastname, email, phone, birthday):
    user_id = "123123123"

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    browser = webdriver.Chrome(options=options)

    try:
        browser.get("https://b24-iu5stq.bitrix24.site/backend_test/")
        time.sleep(5)

        inputs = browser.find_elements(By.CLASS_NAME, "b24-form-control")

        inputs[0].send_keys(username)
        inputs[1].send_keys(lastname)

        button = browser.find_element(By.CLASS_NAME, "b24-form-btn")

        button.click()
        time.sleep(2)

        inputs = browser.find_elements(By.CLASS_NAME, "b24-form-control")

        inputs[0].send_keys(email)
        inputs[1].send_keys(phone)

        button = browser.find_elements(By.CLASS_NAME, "b24-form-btn")

        button[1].click()
        time.sleep(2)

        inputs = browser.find_element(By.CLASS_NAME, "b24-form-control")

        inputs.send_keys(birthday)

        button = browser.find_elements(By.CLASS_NAME, "b24-form-btn")

        button[1].click()
        time.sleep(2)

        if not settings.FORMAT_FOR_SAVING_FILE:
            formatted_date_now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        else:
            formatted_date_now = datetime.datetime.now().strftime(settings.FORMAT_FOR_SAVING_FILE)

        browser.save_screenshot(f"screenshots/{formatted_date_now}_{user_id}.png")

    except Exception as _ex:
        print(_ex)
    finally:
        # Close connection
        browser.close()
        browser.quit()
