from loguru import logger
from telegrinder import CallbackQuery, Dispatch
from telegrinder.bot.rules import CallbackDataMarkup
from telegrinder.tools import MarkdownFormatter

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
        out = await event.api.edit_message_text(
            event.from_user.id,
            event.message.message_id,
            text=f"Ты решил вылечить: {player}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        logger.debug(out)
    await GameAction.create(game=player.game, player_id=player_id, type=Action.revived)
    await event.api.send_message(player.game.chat_id, "Доктор ходил всю ночь с аптечкой 🤨")
    await check_actions(player.game)
