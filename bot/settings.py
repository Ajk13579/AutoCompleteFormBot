import os

from dotenv import load_dotenv

load_dotenv()

ABSOLUTE_PATH_DIR = os.getenv("ABSOLUTE_PATH_DIR")
FORMAT_FOR_SAVING_FILE = os.getenv("FORMAT_FOR_SAVING_FILE")
