"""parse .env variables"""
from envparse import env

env.read_envfile(".env")
BOT_TOKEN = env.str("BOT_TOKEN")

ADMINS_ID: list[str] = env.str("ADMINS_ID").split(",")
