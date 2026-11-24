import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
DATABASE_URL = os.environ.get("DATABASE_URL", "")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))
SESSION_STRING = os.environ.get("SESSION_STRING", "")
BOT_NAME = os.environ.get("BOT_NAME", "Auto Filter Bot")
RESULTS_PER_PAGE = int(os.environ.get("RESULTS_PER_PAGE", 10))
