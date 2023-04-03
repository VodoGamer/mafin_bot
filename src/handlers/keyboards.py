from telegrinder.tools import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup

from src.bot.init import api


async def get_join_game_kb(game_id: int) -> InlineKeyboardMarkup:
    bot = (await api.get_me()).unwrap()
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Присоединиться", url=f"https://t.me/{bot.username}?start=join_{game_id}")
    )
    return keyboard.get_markup()


async def get_bot_redirect_kb() -> InlineKeyboardMarkup:
    bot = (await api.get_me()).unwrap()
    keyboard = InlineKeyboard().add(
        InlineButton("Перейти к боту", f"https://t.me/{bot.username}/")
    )
    return keyboard.get_markup()
