from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup

from src.db.models import Role as GameRole
from src.rules.role import Role

dp = Dispatch()


@dp.callback_query(Role(GameRole.doctor), CallbackDataMarkup("action/<player_id>"))
async def to_heal(event: CallbackQuery, player_id: int):
    await event.answer(str(player_id))


@dp.callback_query(Role(GameRole.mafia), CallbackDataMarkup("action/<player_id>"))
async def to_kill(event: CallbackQuery, player_id: int):
    await event.answer(str(player_id))
