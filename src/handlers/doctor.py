from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup

from src.db.models import Role as GameRole
from src.handlers.day import check_actions
from src.handlers.night import make_night_action
from src.rules import RoleCallback

dp = Dispatch()


@dp.callback_query(
    RoleCallback(GameRole.doctor), CallbackDataMarkup("game/<game_id>/action/<player_id>")
)
async def doctor_heal(event: CallbackQuery, game_id: int, player_id: int):
    game = await make_night_action(event, game_id, player_id, "Ты решил лечить: ")
    await event.api.send_message(game.chat_id, "Доктор ходил всю ночь с аптечкой 🤨")
    await check_actions(game)
