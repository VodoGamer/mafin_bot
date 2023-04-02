"""parse .env variables"""
from envparse import env

env.read_envfile(".env")
BOT_TOKEN = env.str("BOT_TOKEN")

DB_HOST = env.str("POSTGRES_HOST")
DB_PASSWORD = env.str("POSTGRES_PASSWORD")
DB_USER = env.str("POSTGRES_USER")
DB_TITLE = env.str("POSTGRES_DB")

DB_CONNECT = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_TITLE}"
