from datetime import datetime
from enum import Enum, IntEnum

from telegrinder.tools import MarkdownFormatter
from tortoise import fields
from tortoise.models import Model


class GameState(IntEnum):
    set_in_game = 0
    day = 1
    night = 2


class MessagePayload(IntEnum):
    set_in_game = 0
    timer = 1


class Role(Enum):
    died = "Мёртв"
    civilian = "Мирный житель"
    don = "Дон"
    mafia = "Мафия"
    commissioner = "Комиссар"
    doctor = "Доктор"


class Game(Model):
    id: int = fields.IntField(pk=True)
    chat_id: int = fields.BigIntField()
    state: GameState = fields.IntEnumField(GameState)
    start_date: datetime = fields.DatetimeField(auto_now_add=True)
    messages: fields.ReverseRelation["GameMessage"]
    players: fields.ReverseRelation["Player"]
    actions: fields.ReverseRelation["GameAction"]
    votes: fields.ReverseRelation["Vote"]


class GameMessage(Model):
    message_id: int = fields.IntField()
    payload: MessagePayload = fields.IntEnumField(MessagePayload)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="messages"
    )

    class Meta:
        table = "game_message"


class Player(Model):
    id: int = fields.BigIntField(pk=True)
    name: str = fields.CharField(150)
    role: Role | None = fields.CharEnumField(Role, null=True)
    votes: fields.ReverseRelation["Vote"]

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )
    game_actions: fields.ReverseRelation["GameAction"]

    def __str__(self) -> str:
        return MarkdownFormatter(self.name).link(f"tg://user?id={self.id}")


class Vote(Model):
    id: int = fields.IntField(pk=True)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="votes"
    )
    goal_user: fields.ForeignKeyRelation[Player] = fields.ForeignKeyField(
        "models.Player", related_name="votes"
    )


class Action(Enum):
    kill = "убили"
    revived = "возрадили"


class GameAction(Model):
    id: int = fields.IntField(pk=True)
    type: Action = fields.CharEnumField(Action)

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="actions"
    )
    player: fields.ForeignKeyRelation[Player] = fields.ForeignKeyField(
        "models.Player", related_name="game_actions"
    )

    class Meta:
        table = "game_action"
