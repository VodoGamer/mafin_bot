import asyncio
from datetime import datetime, timezone

from loguru import logger
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Game, GameMessage, GameState, MessagePayload
from src.handlers.set_in_game import SET_IN_GAME_TIME
from src.handlers.start import start_game


async def check_timers():
    while True:
        games = await Game.filter(state=GameState.set_in_game).prefetch_related(
            "players", "messages"
        )
        logger.debug(f"{games=}")
        for game in games:
            now = datetime.now(tz=timezone.utc)
            start_date = game.start_date + SET_IN_GAME_TIME
            if start_date < now:
                await start_game(game)
            elif start_date - now <= SET_IN_GAME_TIME / 2:
                await send_or_update_timer(game, (start_date - now).seconds)
        await asyncio.sleep(10)


async def send_or_update_timer(game: Game, seconds: int):
    text = MarkdownFormatter("До начала игры").bold() + " осталось {} секунд"
    timer = await GameMessage.get_or_none(game=game, payload=MessagePayload.timer)

    if timer:
        await api.edit_message_text(
            game.chat_id,
            timer.message_id,
            text=text.format(seconds),
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        return
    message = await api.send_message(
        game.chat_id, text.format(seconds), parse_mode=MarkdownFormatter.PARSE_MODE
    )
    await GameMessage.create(
        game=game, payload=MessagePayload.timer, message_id=message.unwrap().message_id
    )
