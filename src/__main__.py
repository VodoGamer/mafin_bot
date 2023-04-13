"""entry point"""
import asyncio

from src.set_commands import update_bot_settings_list

from .bot.init import bot, dispatch
from .config.db import db_init
from .handlers import dps

loop = asyncio.new_event_loop()
for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch = dispatch

loop.run_until_complete(db_init())
loop.run_until_complete(update_bot_settings_list())
bot.run_forever()
