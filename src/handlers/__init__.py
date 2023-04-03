"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import day, doctor, force_stop, mafia, night, recruiting, start_game, voting

dps: Iterable["Dispatch"] = (
    force_stop.dp,
    recruiting.dp,
    start_game.dp,
    doctor.dp,
    mafia.dp,
    night.dp,
    day.dp,
    voting.dp,
)
