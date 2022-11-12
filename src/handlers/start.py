from random import choice

from loguru import logger
from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text
from telegrinder.tools import MarkdownFormatter
from tortoise import fields

from src.bot.init import api
from src.db.models import Game, GameState, Player, Role
from src.handlers.night import start_night

dp = Dispatch()


@dp.message(Text("/start_game"))
async def force_start(message: Message):
    await api.delete_message(message.chat.id, message.message_id)
    game = await Game.get_or_none(chat_id=message.chat.id).prefetch_related("players", "messages")
    if game and game.state == GameState.set_in_game:
        await start_game(game)


async def start_game(game: Game):
    """начинает игру

    Args:
        game (Game): должен быть `.prefetch_related("players", "messages")`
    """
    for message in game.messages:
        await api.delete_message(game.chat_id, message.message_id)
        await message.delete()

    if len(game.players) < 2:
        await api.send_message(
            game.chat_id,
            f"{MarkdownFormatter('Никто не пришёл').italic()} "
            f"{MarkdownFormatter('на сходку(((').escape()}\n{len(game.players)}\nДля старта игры"
            " необходимо 4 игрока",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        await game.delete()
        return
    game.state = GameState.night
    await game.save()
    await api.send_message(
        game.chat_id,
        MarkdownFormatter("ИГРА НАЧИНАЕТСЯ").bold(),
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
    await give_roles(game)
    await start_night(game)


async def give_roles(game: Game):
    """
    Args:
        game (Game): должен быть `.prefetch_related("players")`
    """
    mafia_count = len(game.players) // 3
    await give_role(game.players, mafia_count, Role.mafia)
    await give_role(game.players, 1, Role.doctor)


async def give_role(players: fields.ReverseRelation[Player], count: int, role: Role):
    while count > 0:
        user = choice(players)
        if user.role != Role.civilian:
            continue
        user.role = role
        await user.save()
        logger.debug(f"give {role=} for {user=}")
        count -= 1
