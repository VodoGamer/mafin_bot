from telegrinder import ABCMessageRule, ABCRule, CallbackQuery, Message

from src.db.models import Life, Player


class LifeCallback(ABCRule[CallbackQuery]):
    def __init__(self, life: Life) -> None:
        self.life = life

    async def check(self, event: CallbackQuery, ctx: dict):
        player = await Player.get_or_none(id=event.callback_query.from_.id, life=self.life)
        return player


class LifeRule(ABCMessageRule):
    def __init__(self, life: Life) -> None:
        self.life = life

    async def check(self, message: Message, ctx: dict):
        player = await Player.get_or_none(id=message.from_user.id, life=self.life)
        return player
