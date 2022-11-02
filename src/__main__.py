"""entry point"""
import asyncio

from loguru import logger

from src.handlers.timer import check_timers

from .bot.init import bot
from .config.db import db_init
from .handlers import dps

loop = asyncio.new_event_loop()
for dp in dps:
    bot.dispatch.message.handlers.extend(dp.message.handlers)
    bot.dispatch.default_handlers.extend(dp.default_handlers)
    bot.dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch.message.middlewares.extend([])


loop.run_until_complete(db_init())
loop.create_task(bot.run_polling())
loop.create_task(check_timers())
try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.info("KeyboardInterrupt")
