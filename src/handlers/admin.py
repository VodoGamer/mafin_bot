from telegrinder import Dispatch, Message
from telegrinder.rules import Text

from src.rules import IsAdmin
from src.services import delete_chat

dp = Dispatch()


@dp.message(IsAdmin(), Text("/delete_chat"))
async def delete_chat_command(message: Message):
    await delete_chat(message.chat.id)
    await message.reply(f"{message.chat.id=} deleted")
