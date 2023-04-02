"""bot init"""
from telegrinder import API, Dispatch, Telegrinder, Token

from src.config.env import BOT_TOKEN

api = API(token=Token(BOT_TOKEN))
dispatch = Dispatch()
bot = Telegrinder(api)
