from datetime import datetime
from enum import Enum, IntEnum

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


class GameMessage(Model):
    message_id: int = fields.IntField()
    payload: MessagePayload = fields.IntEnumField(MessagePayload)
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="messages"
    )

    class Meta:
        table = "game_message"


class Player(Model):
    uid: int = fields.BigIntField()
    username: str = fields.CharField(150)
    role: Role | None = fields.CharEnumField(Role, null=True)

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )

    def __str__(self) -> str:
        return self.username
