"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import day, doctor, end, mafia, night, recruiting, start, stop, voting

dps: Iterable["Dispatch"] = (
    stop.dp,
    recruiting.dp,
    start.dp,
    doctor.dp,
    mafia.dp,
    night.dp,
    day.dp,
    voting.dp,
    end.dp,
)
