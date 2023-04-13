"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import admin, enrollment, join_game, start_bot

dps: Iterable["Dispatch"] = (admin.dp, start_bot.dp, enrollment.dp, join_game.dp)
