import asyncio
from datetime import datetime, timezone

from src.db.models import Game, GameState
from src.handlers.set_in_game import SET_IN_GAME_TIME, send_or_update_timer
from src.handlers.start import start_game


async def send_timers():
    while True:
        games = await Game.filter(state=GameState.set_in_game)
        for game in games:
            now = datetime.now(tz=timezone.utc)
            start_date = game.start_date + SET_IN_GAME_TIME
            if start_date < now:
                await start_game(game)
            elif start_date - now <= SET_IN_GAME_TIME / 2:
                await send_or_update_timer(game, (start_date - now).seconds)
        await asyncio.sleep(10)
