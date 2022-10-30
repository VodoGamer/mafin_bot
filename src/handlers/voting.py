from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataMarkup

from src.bot.init import api

dp = Dispatch()


@dp.callback_query(CallbackDataMarkup("vote/<player_id>"))
async def vote(event: CallbackQuery, player_id: int):
    await api.send_message(event.from_user.id, f"u choice {player_id}")
