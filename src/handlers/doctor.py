from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup

from src.db.models import Action, Game, GameAction
from src.db.models import Role as GameRole
from src.handlers.day import check_actions
from src.rules import RoleCallback

dp = Dispatch()


@dp.callback_query(
    RoleCallback(GameRole.doctor), CallbackDataMarkup("game/<game_id>/action/<player_id>")
)
async def doctor_heal(event: CallbackQuery, game_id: int, player_id: int):
    game = await Game.get(id=game_id)
    if event.message:
        await event.api.edit_message_text(
            event.from_user.id, event.message.message_id, text=f"u choice placeholder: {player_id}"
        )
    await GameAction.create(game=game, player_id=player_id, type=Action.revived)
    await event.api.send_message(game.chat_id, "doctor placeholder")
    await check_actions(game)
