"""entry point"""
import asyncio

from .bot.init import bot
from .config.db import db_init
from .handlers import dps
from .middlewares.example import ExampleMiddleware

loop = asyncio.new_event_loop()
for dp in dps:
    bot.dispatch.message.handlers.extend(dp.message.handlers)
    bot.dispatch.default_handlers.extend(dp.default_handlers)
    bot.dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch.message.middlewares.extend([ExampleMiddleware()])


loop.run_until_complete(db_init())
bot.run_forever()
