from django.conf import settings
import requests


def check_form_availability():
    """Checks whether the site is available for submitting the form"""
    response = requests.get(settings.URL_FORM)
    return response.status_code == 200
