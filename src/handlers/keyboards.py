from uuid import UUID

from telegrinder.tools import InlineButton, InlineKeyboard
from telegrinder.types import InlineKeyboardMarkup

from src.bot.init import gettext as _


def get_join_game_kb(game_id: UUID, bot_username: str | None = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton(
            _("join game button"), url=f"https://t.me/{bot_username}?start=join_{game_id}"
        )
    )
    return keyboard.get_markup()
