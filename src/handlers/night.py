from telegrinder import Dispatch, Message

from src.db.models import GameState
from src.rules.state import State

dp = Dispatch()


@dp.message(State(GameState.night))
async def night(message: Message):
    await message.api.delete_message(message.chat.id, message.message_id)
