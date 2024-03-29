import asyncio
import pathlib

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.tools import MarkdownFormatter
from telegrinder.types import InputFile

from src.bot.init import api
from src.db.models import (
    Action,
    Day,
    Game,
    GameAction,
    GameMessage,
    GameState,
    Life,
    MessagePayload,
    Player,
    Role,
)
from src.handlers.end import check_for_the_end
from src.handlers.keyboards import get_bot_redirect_kb
from src.handlers.services import get_active_players, get_alive_players
from src.rules import LifeRule, State

dp = Dispatch()


class ActiveRole:
    def __init__(self, id: int, role: Role) -> None:
        self.id = id
        self.role = role

    def make_night_action(self):
        ...


@dp.message(State(GameState.day), LifeRule(Life.died))
async def day(message: Message):
    await api.delete_message(message.chat.id, message.message_id)


async def start_day(game: Game):
    await Day.create(game=game)
    messages = await GameMessage.filter(game=game, payload=MessagePayload.night_action)
    for message in messages:
        await api.delete_message(message.chat_id, message.message_id)
        await message.delete()
    game.state = GameState.day
    await game.save()
    await make_night_actions(game)
    if await check_for_the_end(game):
        return
    await api.send_message(chat_id=game.chat_id, text="Наступает день.\n")
    await asyncio.sleep(45)
    await start_voting(game)


async def start_voting(game: Game):
    players = await get_alive_players(game)
    keyboard = InlineKeyboard()
    for player in players:
        for kb_player in players:
            if kb_player == player:
                continue
            keyboard.add(
                InlineButton(kb_player.name, callback_data=f"game/{game.id}/vote/{kb_player.id}")
            )
            keyboard.row()

        result = await api.send_message(
            chat_id=player.id, text="голосование кого кикнуть:", reply_markup=keyboard.get_markup()
        )
        await GameMessage.create(
            message_id=result.unwrap().message_id,
            payload=MessagePayload.voting,
            chat_id=player.id,
            game=game,
        )
    keyboard = await get_bot_redirect_kb()
    await api.send_message(
        chat_id=game.chat_id,
        text="Начато голосование за кик: ",
        reply_markup=keyboard,
    )


async def make_night_actions(game: Game):
    killed = await GameAction.get_or_none(type=Action.kill, game=game).prefetch_related("player")
    revived = await GameAction.get_or_none(type=Action.revived, game=game).prefetch_related(
        "player"
    )
    if killed:
        await api.send_message(
            chat_id=killed.player.id,
            text="Тебя убили :(\nТы можешь написать предсмертное сообщение сюда",
        )
        killed.player.life = Life.died
        await killed.player.save(update_fields=("life",))
    if revived:
        doctor = await Player.get(game=game, role=Role.doctor)
        if doctor != revived.player:
            await api.send_message(chat_id=revived.player.id, text="Доктор приходил к тебе ночью")
        await revived.player.save(update_fields=("life",))

    await send_actions(game, killed, revived)


async def send_actions(game: Game, killed: GameAction | None, revived: GameAction | None):
    if not killed or (killed and revived and killed.player.id == revived.player.id):
        await api.send_photo(
            game.chat_id,
            caption="Сегодня все выжили!",
            photo=InputFile("alive.jpg", pathlib.Path("src/images/alive.jpg").read_bytes()),
        )
    else:
        await api.send_photo(
            game.chat_id,
            caption=f"Сегодня ночью убили: {killed.player}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
            photo=InputFile("kill.jpg", pathlib.Path("src/images/kill.jpg").read_bytes()),
        )


async def check_actions(game: Game):
    active_roles = await get_active_players(game)
    actions = await GameAction.filter(game=game)
    if len(active_roles) == len(actions):
        await start_day(game)
