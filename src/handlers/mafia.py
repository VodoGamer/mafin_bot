from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.bot.rules import CallbackDataMarkup, IsPrivate
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Action, Game, GameAction, Player
from src.db.models import Role as GameRole
from src.handlers.day import check_actions
from src.rules import RoleCallback, RoleRule

dp = Dispatch()


@dp.callback_query(
    RoleCallback(GameRole.mafia), CallbackDataMarkup("game/<game_id>/action/<player_id>")
)
async def mafia_kill(event: CallbackQuery, game_id: int, player_id: int):
    game = await Game.get(id=game_id)
    if event.message:
        await event.api.edit_message_text(
            event.from_user.id, event.message.message_id, text=f"u choice placeholder: {player_id}"
        )
    await GameAction.create(game=game, player_id=player_id, type=Action.kill)
    await event.api.send_message(game.chat_id, "mafia placeholder")
    await check_actions(game)


@dp.message(IsPrivate(), RoleRule(GameRole.mafia))
async def mafia_communication(message: Message):
    if not message.text:
        return
    player = await Player.get(id=message.from_user.id).prefetch_related("game")
    mafias = await Player.filter(game=player.game).exclude(id=player.id)
    for mafia in mafias:
        await api.send_message(
            mafia.id,
            f"{str(player)} сказал: {message.text}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
