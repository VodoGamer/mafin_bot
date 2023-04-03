import asyncio
from datetime import datetime, timedelta, timezone

from loguru import logger
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Day, Game, GameMessage, GameState, MessagePayload, Night
from src.handlers.config import SET_IN_GAME_TIME
from src.handlers.day import start_day
from src.handlers.start import start_game
from src.handlers.voting import end_day


async def check_timers():
    while True:
        games = await Game.all()
        for game in games:
            await check_game_timers(game)
        await asyncio.sleep(10)


async def check_game_timers(game: Game):
    now = datetime.now(tz=timezone.utc)
    timers = Timers(game, now)
    if game.state == GameState.recruiting:
        await timers.check_set_in_games()
    elif game.state == GameState.night:
        await timers.check_nights()
    elif game.state == GameState.day:
        await timers.check_days()


class Timers:
    def __init__(self, game: Game, now: datetime) -> None:
        self.game = game
        self.now = now

    async def check_set_in_games(self):
        logger.debug(f"{self.game=} {self.game.start_date=}")
        beginning_date = self.game.start_date + SET_IN_GAME_TIME
        if beginning_date <= self.now:
            return await start_game(self.game)

        remaining_time = beginning_date - self.now
        if remaining_time.seconds <= 10:
            await asyncio.sleep(10 - remaining_time.seconds)
            return await start_game(self.game)

        timer = await GameMessage.get_or_none(game=self.game, payload=MessagePayload.timer)
        if not timer and remaining_time >= SET_IN_GAME_TIME / 2:
            return
        await send_or_update_timer(self.game, timer, remaining_time.seconds)

    async def check_nights(self):
        night = await Night.filter(game=self.game).order_by("-id").first()
        if night and night.start_date + timedelta(seconds=60) <= self.now:
            logger.debug(f"{night=} {night.start_date=}")
            await start_day(self.game)

    async def check_days(self):
        day = await Day.filter(game=self.game).order_by("-id").first()
        if day and day.start_date + timedelta(seconds=80) <= self.now:
            logger.debug(f"{day=} {day.start_date=}")
            await end_day(self.game)


async def send_or_update_timer(game: Game, timer: GameMessage | None, seconds: int):
    text = MarkdownFormatter("До начала игры").bold() + " осталось {} секунд\\(ы\\)"

    if timer:
        return await api.edit_message_text(
            game.chat_id,
            timer.message_id,
            text=text.format(seconds),
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
    message = await api.send_message(
        chat_id=game.chat_id, text=text.format(seconds), parse_mode=MarkdownFormatter.PARSE_MODE
    )
    await GameMessage.create(
        game=game, payload=MessagePayload.timer, message_id=message.unwrap().message_id
    )
