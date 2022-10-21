"""init tortoise-orm"""
from tortoise import Tortoise

from src.config.env import DB_CONNECT

TORTOISE_ORM = {
    "connections": {"default": DB_CONNECT},
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def db_init():
    await Tortoise.init(TORTOISE_ORM)


async def db_shutdown():
    await Tortoise.close_connections()
