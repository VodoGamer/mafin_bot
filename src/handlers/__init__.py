"""list of all dispatchers"""
from typing import Iterable

from telegrinder import Dispatch

from . import start

dps: Iterable["Dispatch"] = (start.dp,)
