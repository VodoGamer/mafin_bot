"""bot init"""
from telegrinder import API, Telegrinder, Token

from src.config.env import BOT_TOKEN

api = API(token=Token(BOT_TOKEN))
bot = Telegrinder(api)
