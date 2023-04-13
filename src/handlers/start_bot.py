from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from src.bot.init import formatter
from src.templates import render_template

dp = Dispatch()


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(render_template("start_bot.j2"), parse_mode=formatter.PARSE_MODE)
