import asyncio

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message

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
    await asyncio.sleep(30)
    await start_voting(game)


async def start_voting(game: Game):
    players = await Player.filter(game=game).exclude(role=Role.died)
    keyboard = InlineKeyboard()
    for player in players:
        keyboard.add(InlineButton(player.name, callback_data=f"vote/{player.id}"))
        keyboard.row()
    for player in players:
        await api.send_message(
            player.id, "golosovanie placeholder", reply_markup=keyboard.get_markup()
        )


async def make_night_actions(game):
    kill = await GameAction.get(type=Action.kill).prefetch_related("player")
    await api.send_message(kill.player.id, "u died placeholder")
    kill.player.role = Role.died
    await kill.player.save()
    revived = await GameAction.get(type=Action.revived).prefetch_related("player")
    await api.send_message(revived.player.id, "u revived placeholder")
    if kill.player.id == revived.player.id:
        await api.send_message(game.chat_id, "all alive!!! wow!! placeholder")
        return
    await api.send_message(game.chat_id, f"{kill.player.name} died now!!!")


async def check_actions(game: Game):
    active_roles = await Player.filter(game=game).exclude(role=Role.civilian)
    actions = await GameAction.filter(game=game)
    if len(active_roles) == len(actions):
        await start_day(game)
