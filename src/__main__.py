"""entry point"""
import asyncio

from loguru import logger

from src.handlers.timer import check_timers

from .bot.init import bot, dispatch
from .config.db import db_init
from .handlers import dps

loop = asyncio.new_event_loop()
for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

dispatch.message.middlewares.extend([])
bot.dispatch = dispatch

loop.run_until_complete(db_init())
loop.create_task(bot.run_polling())
loop.create_task(check_timers())
try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt")
