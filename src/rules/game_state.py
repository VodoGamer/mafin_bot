from telegrinder import ABCMessageRule, Message

from src.services.game import GameStatus, get_last_game


class GameStatusRule(ABCMessageRule):
    def __init__(self, status: GameStatus) -> None:
        self.status = status

    async def check(self, message: Message, ctx: dict) -> bool:
        game = await get_last_game(message.chat.id)
        if not game or game.status == self.status.value:
            return True
        return False
