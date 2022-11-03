import asyncio

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from tortoise.expressions import Q

from src.bot.init import api
from src.db.models import Action, Game, GameAction, GameState, Player, Role
from src.rules import RoleRule, State

dp = Dispatch()


@dp.message(State(GameState.day), RoleRule(Role.died))
async def day(message: Message):
    ...
    # await api.delete_message(message.chat.id, message.message_id)


async def start_day(game: Game):
    game.state = GameState.day
    await game.save()
    await make_night_actions(game)
    await api.send_message(game.chat_id, "obsyzhdenie placeholder")
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
            player.id, "golosovanie placeholder", reply_markup=keyboard.get_markup()
        )


async def make_night_actions(game: Game):
    killed = await GameAction.get_or_none(type=Action.kill, game=game).prefetch_related("player")
    revived = await GameAction.get_or_none(type=Action.revived, game=game).prefetch_related(
        "player"
    )
    if not killed or (revived and revived.player == killed.player):
        await api.send_message(game.chat_id, "Все выжили!")
        return
    killed.player.role = Role.died
    await killed.player.save()
    await api.send_message(game.chat_id, f"{killed.player} умер!")


async def check_actions(game: Game):
    active_roles = await Player.filter(game=game).exclude(
        Q(role=Role.civilian) | Q(role=Role.died)
    )
    actions = await GameAction.filter(game=game)
    if len(active_roles) == len(actions):
        await start_day(game)
