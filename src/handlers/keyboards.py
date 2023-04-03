from telegrinder.tools import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup


async def get_join_game_kb(bot_username: str | None, game_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Присоединиться", url=f"https://t.me/{bot_username}?start=join_{game_id}")
    )
    return keyboard.get_markup()
