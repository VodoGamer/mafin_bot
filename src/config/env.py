"""parse .env variables"""
import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS_ID: list[str] = os.getenv("ADMINS_ID", "None").split(",")

# global settings
TIMER_DURATION: int = int(os.getenv("TIMER_DURATION", 30))
TIMERS_UPDATE_FREQUENCY: int = int(os.getenv("TIMERS_UPDATE_FREQUENCY", 5))
