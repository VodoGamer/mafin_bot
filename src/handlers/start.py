import asyncio
from datetime import datetime, timedelta, timezone
from random import choice

from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Text

from src.bot.init import api
from src.db.models import Game, GameMessage, GameState, MessagePayload, Player, Role
from src.handlers.night import start_night

dp = Dispatch()


async def start_timer_to_the_game(timer: timedelta, game: Game):
    start_date = game.start_date + timer
    mention_seconds = round((start_date - datetime.now(tz=timezone.utc)).seconds / 2)

    await asyncio.sleep(mention_seconds)
    new_game = await Game.get_or_none(id=game.id)
    if new_game and new_game.state != GameState.set_in_game:
        return
    result = await api.send_message(
        game.chat_id, f"before the game placeholder {mention_seconds} секунд"
    )
    await GameMessage.create(
        game=game, message_id=result.unwrap().message_id, payload=MessagePayload.timer
    )
    await asyncio.sleep(mention_seconds)
    new_game = await Game.get(id=game.id)
    if new_game and new_game.state != GameState.set_in_game:
        return
    await start_game(game)


@dp.message(Text("/start_game"))
async def force_start(message: Message):
    game = await Game.get_or_none(chat_id=message.chat.id)
    if game and game.state == GameState.set_in_game:
        await start_game(game)


async def start_game(game: Game):
    game = await game.get(id=game.id).prefetch_related("players")
    game.state = GameState.night
    await game.save()
    messages = await GameMessage.filter(game=game)

    for message in messages:
        await api.delete_message(game.chat_id, message.message_id)
        await message.delete()

    if len(game.players) < 1:
        await api.send_message(
            game.chat_id, f"not enough players placeholder: {len(game.players)}"
        )
        await game.delete()
        return
    await api.send_message(game.chat_id, "start game placeholder!")
    await give_roles(game)
    await start_night(game)
    await api.send_message(game.chat_id, "night is coming placeholder!")


async def give_roles(game: Game):
    players = await Player.filter(game=game)
    mafia_count = len(game.players) // 2
    await give_role(players, mafia_count, Role.mafia)
    await give_role(players, 1, Role.doctor)


async def give_role(players: list[Player], count: int, role: Role):
    while count > 0:
        user = choice(players)
        if not user.role:
            user.role = role
            await user.save()
            count -= 1
