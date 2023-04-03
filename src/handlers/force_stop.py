from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from src.bot.init import api
from src.db.models import Game

dp = Dispatch()


@dp.message(Text("/force_stop"))
async def force_stop(message: Message):
    await api.delete_message(message.chat.id, message.message_id)
    game = await Game.get(chat_id=message.chat.id)
    await game.delete()
    await message.reply("удачно!")
