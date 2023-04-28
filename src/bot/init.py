"""bot init"""
import gettext
from pathlib import Path

import edgedb
from loguru import logger
from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.tools import HTMLFormatter

from src.config.env import BOT_TOKEN

formatter = HTMLFormatter
api = API(token=Token(BOT_TOKEN))
dispatch = Dispatch()
bot = Telegrinder(api)

logger = logger
db = edgedb.create_async_client()
gnu_translations = gettext.translation(
    domain="messages", localedir=Path("locale"), languages=["ru_RU"]
)
gettext = gnu_translations.gettext
