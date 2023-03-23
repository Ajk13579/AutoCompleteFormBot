import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
SERVICE_SITE_URL = os.getenv("SERVICE_SITE_URL")
