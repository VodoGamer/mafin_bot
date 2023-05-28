import asyncio
from datetime import datetime, timedelta, timezone

from src.bot.init import api, logger
from src.config.env import TIMER_DURATION, TIMERS_UPDATE_FREQUENCY
from src.handlers.start_game import start_game
from src.services import (
    Game,
    MessagePayload,
    create_message,
    get_enrollment_games,
    get_last_game,
    get_message,
)
from src.templates import render_template


def start_timer_poling(chat_id: int):
    loop = asyncio.get_running_loop()
    loop.create_task(poling_timer(chat_id))


async def send_timer_message(chat_id: int, time: int):
    output = (
        await api.send_message(
            chat_id=chat_id,
            text=render_template("timer.j2", {"time": time}),
        )
    ).unwrap()
    game = await get_last_game(chat_id)
    if not game:
        return
    await create_message(output.message_id, MessagePayload.timer, chat_id, game.id)


async def update_timer_message(chat_id: int, time: timedelta, message_id: int):
    await api.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=render_template("timer.j2", {"time": time.seconds}),
    )


async def delete_timer_message(chat_id: int, message_id: int):
    await api.delete_message(chat_id=chat_id, message_id=message_id)


async def process_timer_for_all_chats():
    games = await get_enrollment_games()
    if not games:
        return
    for game in games:
        start_timer_poling(game.chat.chat_id)


async def poling_timer(chat_id: int):
    game = await get_last_game(chat_id)
    if not game:
        return False
    timer_message = await get_message(game.chat.chat_id, MessagePayload.timer)
    if not timer_message:
        return False
    while True:
        remaining_delta = get_timer_remaining_delta(game)
        await update_timer_message(
            chat_id=chat_id, time=remaining_delta, message_id=timer_message.message_id
        )
        logger.debug(
            "remaining_delta({}); TIMERS_UPDATE_FREQUENCY({})",
            remaining_delta,
            TIMERS_UPDATE_FREQUENCY,
        )
        if datetime.now(tz=timezone.utc) > get_game_start_date(game):
            if remaining_delta.seconds <= TIMERS_UPDATE_FREQUENCY:
                await asyncio.sleep(remaining_delta.seconds)
            await delete_timer_message(chat_id, timer_message.message_id)
            await start_game(game.id)
            return None
        await asyncio.sleep(TIMERS_UPDATE_FREQUENCY)
        continue


def get_timer_remaining_delta(game: Game) -> timedelta:
    now = datetime.now(tz=timezone.utc)
    remaining_time = get_game_start_date(game) - now
    logger.debug("timer remaining_delta: {}", remaining_time)
    return remaining_time


def get_game_start_date(game: Game) -> datetime:
    return game.start_date + timedelta(seconds=TIMER_DURATION)
