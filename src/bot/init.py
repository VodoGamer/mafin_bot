"""bot init"""
import edgedb
from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.tools import HTMLFormatter

from src.config.env import BOT_TOKEN

formatter = HTMLFormatter
api = API(token=Token(BOT_TOKEN))
dispatch = Dispatch()
bot = Telegrinder(api)

db = edgedb.create_async_client()
