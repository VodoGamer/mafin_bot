"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import day, doctor, mafia, night, set_in_game, start

dps: Iterable["Dispatch"] = (set_in_game.dp, start.dp, doctor.dp, mafia.dp, night.dp, day.dp)
