from datetime import datetime
from enum import Enum, IntEnum

from telegrinder.tools import MarkdownFormatter
from tortoise import fields
from tortoise.models import Model


class GameState(IntEnum):
    set_in_game = 0
    day = 1
    night = 2


class Game(Model):
    id: int = fields.IntField(pk=True)
    chat_id: int = fields.BigIntField()
    state: GameState = fields.IntEnumField(GameState)
    start_date: datetime = fields.DatetimeField(auto_now_add=True)
    messages: fields.ReverseRelation["GameMessage"]
    players: fields.ReverseRelation["Player"]
    actions: fields.ReverseRelation["GameAction"]
    votes: fields.ReverseRelation["Vote"]
    nights: fields.ReverseRelation["Night"]
    days: fields.ReverseRelation["Day"]


class MessagePayload(IntEnum):
    set_in_game = 0
    timer = 1
    night_action = 2
    voting = 3


class GameMessage(Model):
    message_id: int = fields.IntField()
    payload: MessagePayload = fields.IntEnumField(MessagePayload)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="messages"
    )
    chat_id: int | None = fields.BigIntField(null=True)

    class Meta:
        table = "game_message"


class Role(Enum):
    civilian = "Мирный житель"
    don = "Дон"
    mafia = "Мафия"
    commissioner = "Комиссар"
    doctor = "Доктор"


class Life(IntEnum):
    died = 0
    alive = 1


class Player(Model):
    id: int = fields.BigIntField(pk=True)
    name: str = fields.CharField(150)
    role: Role = fields.CharEnumField(Role, default=Role.civilian)
    life: Life = fields.IntEnumField(Life, default=Life.alive)
    votes: fields.ReverseRelation["Vote"]

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )
    game_actions: fields.ReverseRelation["GameAction"]

    def __str__(self) -> str:
        return MarkdownFormatter(self.name).mention(self.id)


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
    revived = "возродили"


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


class Night(Model):
    id: int = fields.IntField(pk=True)
    start_date: datetime = fields.DatetimeField(auto_now_add=True)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="nights"
    )


class Day(Model):
    id: int = fields.IntField(pk=True)
    start_date: datetime = fields.DatetimeField(auto_now_add=True)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="days"
    )
