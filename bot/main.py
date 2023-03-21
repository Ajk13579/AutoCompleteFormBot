import datetime
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import settings


def complete_form(url: str) -> None:
    """Fills out the form at a certain specified URL address"""

    username = "username"
    lastname = "lastname"
    email = "email@gmail.com"
    phone = "+93-68-0"
    birthday = "10.03.2023"

    user_id = "123123123"

    # Create a driver (browser)
    browser = webdriver.Chrome()

    try:
        browser.get(url)

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

        if not Path(settings.ABSOLUTE_PATH_DIR).exists():
            Path(settings.ABSOLUTE_PATH_DIR).mkdir()

        browser.save_screenshot(f"{settings.ABSOLUTE_PATH_DIR}/{formatted_date_now}_{user_id}.png")

    except Exception as _ex:
        print(_ex)
    finally:
        # Close connection
        browser.quit()


def main():
    url = "https://b24-iu5stq.bitrix24.site/backend_test/"
    complete_form(url)


if __name__ == '__main__':
    main()
