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
    keyboard = await get_keyboard_to_bot()
    await api.send_message(
        game.chat_id, "Начато голосование за кик: ", reply_markup=keyboard.get_markup()
    )


async def get_keyboard_to_bot():
    bot = (await api.get_me()).unwrap().username
    keyboard = InlineKeyboard().add(InlineButton("Перейти к боту", f"https://t.me/{bot}/"))
    return keyboard


async def make_night_actions(game: Game):
    killed = await GameAction.get_or_none(type=Action.kill, game=game).prefetch_related("player")
    revived = await GameAction.get_or_none(type=Action.revived, game=game).prefetch_related(
        "player"
    )
    if killed:
        await api.send_message(
            killed.player.id, "Тебя убили :(\nТы можешь написать предсмертное сообщение сюда"
        )
        killed.player.role = Role.died
        await killed.player.save(update_fields=("role",))
    if revived:
        await api.send_message(revived.player.id, "Доктор приходил к тебе ночью")
        await revived.player.save(update_fields=("role",))

    await send_actions(game, killed, revived)


async def send_actions(game: Game, killed: GameAction | None, revived: GameAction | None):
    if not killed or (killed and revived and killed.player.id == revived.player.id):
        await api.send_message(game.chat_id, "Сегодня все выжили!")
    else:
        await api.send_message(
            game.chat_id,
            f"Сегодня ночью убили: {killed.player}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )


async def check_actions(game: Game):
    active_roles = await Player.filter(game=game).exclude(
        Q(role=Role.civilian) | Q(role=Role.died)
    )
    actions = await GameAction.filter(game=game)
    if len(active_roles) == len(actions):
        await start_day(game)
