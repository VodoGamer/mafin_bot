"""entry point"""
import asyncio

from src.handlers.timers import process_timer_for_all_chats
from src.set_commands import update_bot_settings_list

from .bot.init import bot, dispatch, logger
from .handlers import dps

loop = asyncio.new_event_loop()
for dp in dps:
    dispatch.message.handlers.extend(dp.message.handlers)
    dispatch.default_handlers.extend(dp.default_handlers)
    dispatch.callback_query.handlers.extend(dp.callback_query.handlers)

bot.dispatch = dispatch

loop.run_until_complete(update_bot_settings_list())
loop.create_task(bot.run_polling())
loop.create_task(process_timer_for_all_chats())
try:
    loop.run_forever()
except KeyboardInterrupt:
    logger.error("KeyboardInterrupt")
