from telegrinder import ABCMessageRule, ABCRule, CallbackQuery, Message

from src.db.models import Player
from src.db.models import Role as GameRole


class RoleCallback(ABCRule[CallbackQuery]):
    def __init__(self, role: GameRole) -> None:
        self.role = role

    async def check(self, event: CallbackQuery, ctx: dict):
        player = await Player.get_or_none(id=event.callback_query.from_.id, role=self.role)
        return player


class RoleRule(ABCMessageRule):
    def __init__(self, role: GameRole) -> None:
        self.role = role

    async def check(self, message: Message, ctx: dict):
        player = await Player.get_or_none(id=message.from_user.id, role=self.role)
        return player
