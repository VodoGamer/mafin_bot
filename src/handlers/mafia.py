from telegrinder import CallbackQuery, Dispatch, Message
from telegrinder.bot.rules import CallbackDataMarkup, IsPrivate
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Action, Player
from src.db.models import Role as GameRole
from src.handlers.day import check_actions
from src.handlers.night import make_night_action
from src.rules import RoleCallback, RoleRule

dp = Dispatch()


@dp.callback_query(
    RoleCallback(GameRole.don), CallbackDataMarkup("game/<game_id>/action/<player_id>")
)
async def mafia_kill(event: CallbackQuery, game_id: int, player_id: int):
    game = await make_night_action(event, game_id, player_id, "Ты решил зарезать: ", Action.kill)
    await event.api.send_message(chat_id=game.chat_id, text="Мафия решила кого-то зарезать")
    await check_actions(game)


@dp.message(IsPrivate(), RoleRule(GameRole.don))
async def mafia_communication(message: Message):
    if not message.text:
        return
    player = await Player.get(id=message.from_user.id).prefetch_related("game")
    mafias = await Player.filter(game=player.game).exclude(id=player.id)
    for mafia in mafias:
        await api.send_message(
            chat_id=mafia.id,
            text=f"{player} сказал: {message.text}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
