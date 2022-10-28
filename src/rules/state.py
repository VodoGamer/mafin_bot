from telegrinder import ABCMessageRule, Message

from src.db.models import Game, GameState


class State(ABCMessageRule):
    def __init__(self, state: GameState) -> None:
        self.state = state

    async def check(self, message: Message, ctx: dict):
        game = await Game.get_or_none(chat_id=message.chat.id, state=self.state)
        return game
