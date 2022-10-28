"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import set_in_game, start

dps: Iterable["Dispatch"] = (set_in_game.dp, start.dp)
