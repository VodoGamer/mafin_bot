"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import day, doctor, end, mafia, night, set_in_game, start, stop, voting

dps: Iterable["Dispatch"] = (
    stop.dp,
    set_in_game.dp,
    start.dp,
    doctor.dp,
    mafia.dp,
    night.dp,
    day.dp,
    voting.dp,
    end.dp,
)
