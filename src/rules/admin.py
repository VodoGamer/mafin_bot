from telegrinder import ABCMessageRule, Message

from src.config.env import ADMINS_ID


class IsAdmin(ABCMessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        if str(message.from_user.id) in ADMINS_ID:
            return True
        return False
