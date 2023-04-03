from random import choice

from loguru import logger
from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Game, GameMessage, GameState, Player, Role
from src.handlers.night import start_night

dp = Dispatch()


@dp.message(Text("/start_game"))
async def force_start(message: Message):
    await api.delete_message(message.chat.id, message.message_id)
    game = await Game.get_or_none(chat_id=message.chat.id)
    if game and game.state == GameState.recruiting:
        await start_game(game)


async def start_game(game: Game):
    players = await Player.filter(game=game)
    messages = await GameMessage.filter(game=game)
    for message in messages:
        await api.delete_message(game.chat_id, message.message_id)
        await message.delete()

    if len(players) <= 3:
        await api.send_message(
            chat_id=game.chat_id,
            text=f"{MarkdownFormatter('Никто не пришёл').italic()} "
            f"{MarkdownFormatter('на сходку(((').escape()}\n\nДля старта игры"
            " необходимо 4 игрока",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        await game.delete()
        return
    game.state = GameState.night
    await game.save()
    await api.send_message(
        chat_id=game.chat_id,
        text=MarkdownFormatter("ИГРА НАЧИНАЕТСЯ").bold(),
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
    await give_roles(players)
    await send_role_notice(players)
    await start_night(game)


async def send_role_notice(players: list[Player]):
    for player in players:
        await api.send_message(
            chat_id=player.id,
            text=f"Ты — {MarkdownFormatter(player.role.value).italic()}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )


async def give_roles(players: list[Player]):
    await give_role(players, 1, Role.don)
    await give_role(players, 1, Role.doctor)
    mafia_count = len(players) // 4 - 1
    await give_role(players, mafia_count, Role.mafia)


async def give_role(players: list[Player], count: int, role: Role):
    while count > 0:
        user = choice(players)
        if user.role != Role.civilian:
            continue
        user.role = role
        await user.save()
        logger.debug(f"give {role=} for {user=}")
        count -= 1
