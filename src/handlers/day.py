import asyncio

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.tools import MarkdownFormatter
from tortoise.expressions import Q

from src.bot.init import api
from src.db.models import Action, Game, GameAction, GameState, Player, Role
from src.handlers.end import check_for_the_end
from src.rules import RoleRule, State

dp = Dispatch()


@dp.message(State(GameState.day), RoleRule(Role.died))
async def day(message: Message):
    await api.delete_message(message.chat.id, message.message_id)


async def start_day(game: Game):
    game.state = GameState.day
    await game.save()
    await make_night_actions(game)
    if await check_for_the_end(game):
        return
    await api.send_message(game.chat_id, "Наступает день.\n")
    await asyncio.sleep(20)
    await start_voting(game)


async def start_voting(game: Game):
    players = await Player.filter(game=game).exclude(role=Role.died)
    keyboard = InlineKeyboard()
    for player in players:
        keyboard.add(InlineButton(player.name, callback_data=f"game/{game.id}/vote/{player.id}"))
        keyboard.row()
    for player in players:
        await api.send_message(
            player.id, "голосование кого кикнуть:", reply_markup=keyboard.get_markup()
        )


async def make_night_actions(game: Game):
    killed_users = await GameAction.filter(type=Action.kill, game=game).prefetch_related("player")
    revived = await GameAction.get_or_none(type=Action.revived, game=game).prefetch_related(
        "player"
    )
    killed_count = 0
    for user in killed_users:
        if revived and revived.player.id == user.player.id:
            continue
        killed_count += 1
        user.player.role = Role.died
        await user.player.save()
        await api.send_message(game.chat_id, f"{user.player} умер!", MarkdownFormatter.PARSE_MODE)
    if killed_count == 0:
        await api.send_message(game.chat_id, "Все выжили!")
        return


async def check_actions(game: Game):
    active_roles = await Player.filter(game=game).exclude(
        Q(role=Role.civilian) | Q(role=Role.died)
    )
    actions = await GameAction.filter(game=game)
    if len(active_roles) == len(actions):
        await start_day(game)
