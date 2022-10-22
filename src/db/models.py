from enum import Enum, IntEnum
from tortoise import fields
from tortoise.models import Model


class GameState(IntEnum):
    set_in_game = 0
    day = 1
    night = 2
    ended = -1


class Role(Enum):
    civilian = "Мирный житель"
    don = "Дон"
    mafia = "Мафия"
    commissioner = "Комиссар"
    doctor = "Доктор"


class Chat(Model):
    id: int = fields.BigIntField(pk=True)
    games: fields.ReverseRelation["Game"]


class Game(Model):
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat", related_name="games"
    )
    state: GameState | None = fields.IntEnumField(GameState, null=True)
    players: fields.ReverseRelation["Player"]


class Player(Model):
    uid: int = fields.BigIntField()
    role: Role | None = fields.CharEnumField(Role, null=True)

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )
