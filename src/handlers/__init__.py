"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import doctor, night, set_in_game, start, mafia

dps: Iterable["Dispatch"] = (set_in_game.dp, start.dp, doctor.dp, mafia.dp, night.dp)
