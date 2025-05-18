import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")