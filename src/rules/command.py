from typing import Iterable

from telegrinder import ABCMessageRule, Message


class ChatCommand(ABCMessageRule):
    def __init__(self, command: str | Iterable[str]) -> None:
        self.commands = [command] if isinstance(command, str) else command

    async def check(self, message: Message, ctx: dict):
        for command in self.commands:
            if message.text and (
                message.text.startswith(command + "@") or message.text.startswith(command)
            ):
                if message.chat.type == "private":
                    await message.reply("Эта команда доступна только в чате!")
                    return False
                return True
