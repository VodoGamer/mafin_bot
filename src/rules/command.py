from typing import Iterable

from telegrinder import ABCMessageRule, Message


class Command(ABCMessageRule):
    def __init__(self, command: str | Iterable[str]) -> None:
        self.commands = [command] if isinstance(command, str) else command

    async def check(self, message: Message, ctx: dict):
        for command in self.commands:
            if message.text and message.text.startswith(command):
                return True
        return False
