import asyncio
from datetime import datetime, timedelta, timezone

from telegrinder import Dispatch

from src.bot.init import api
from src.db.models import Game

dp = Dispatch()


async def start_timer_to_the_game(timer: timedelta, game: Game):
    start_date = game.start_date + timer
    mention_seconds = round((start_date - datetime.now(tz=timezone.utc)).seconds / 2)
    await asyncio.sleep(mention_seconds)
    await api.send_message(game.chat_id, f"before the game placeholder {mention_seconds} секунд")
