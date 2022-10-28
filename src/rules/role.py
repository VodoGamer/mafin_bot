from telegrinder import ABCRule, CallbackQuery

from src.db.models import Player
from src.db.models import Role as GameRole


class Role(ABCRule[CallbackQuery]):
    def __init__(self, role: GameRole) -> None:
        self.role = role

    async def check(self, event: CallbackQuery, ctx: dict):
        player = await Player.get_or_none(id=event.callback_query.from_.id)
        return player and player.role == self.role
