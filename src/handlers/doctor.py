from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup

from src.db.models import Action, GameAction, Player
from src.db.models import Role as GameRole
from src.handlers.day import check_actions
from src.rules import RoleCallback

dp = Dispatch()


@dp.callback_query(
    RoleCallback(GameRole.doctor), CallbackDataMarkup("game/<game_id>/action/<player_id>")
)
async def doctor_heal(event: CallbackQuery, game_id: int, player_id: int):
    player = await Player.get(game_id=game_id, id=player_id).prefetch_related("game")
    if event.message:
        await event.api.edit_message_text(
            event.from_user.id, event.message.message_id, text=f"Ты решил лечить: {player}"
        )
    await GameAction.create(game=player.game, player_id=player_id, type=Action.revived)
    await event.api.send_message(player.game.chat_id, "Доктор не спал всю ночь и лечил кого-то")
    await check_actions(player.game)
