from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup

from src.db.models import Action, GameAction, Game
from src.db.models import Role as GameRole
from src.rules import Role

dp = Dispatch()


@dp.callback_query(Role(GameRole.doctor), CallbackDataMarkup("game/<game_id>/action/<player_id>"))
async def to_heal(event: CallbackQuery, game_id: int, player_id: int):
    game = await Game.get(id=game_id)
    if event.message:
        await event.api.edit_message_text(
            event.from_user.id, event.message.message_id, text=f"u choice placeholder: {player_id}"
        )
    await GameAction.create(game=game, player_id=player_id, type=Action.revived)
    await event.api.send_message(game.chat_id, "doctor placeholder")
