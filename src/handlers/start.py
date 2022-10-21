from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text

from src.rules.command import Command

dp = Dispatch()

START_COMMAND = "/start_mafin"


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(f"start placeholder\nдля начала игры введите команду \n{START_COMMAND}")


@dp.message(Command(START_COMMAND))
async def start_mafin(message: Message):
    if message.chat.type == "private":
        await message.reply("Игры в мафины доступны только в чате")
        return
    await message.reply("start command placeholder")
