from telegrinder.tools import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup


def get_enrollment_kb(game_id: int, bot_username: str | None = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Присоединиться", url=f"https://t.me/{bot_username}?start=join_{game_id}")
    )
    return keyboard.get_markup()
