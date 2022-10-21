from enum import Enum, IntEnum
from tortoise import fields
from tortoise.models import Model


class ChatStates(IntEnum):
    set_in_game = 0


class GameStates(IntEnum):
    inactive = 0
    day = 1
    night = 2
    ended = -1


class Roles(Enum):
    don = "Дон"
    mafia = "Мафия"
    commissioner = "Комиссар"
    doctor = "Доктор"


class Chat(Model):
    id: int = fields.BigIntField(pk=True)
    state: ChatStates | None = fields.IntEnumField(ChatStates, null=True)
    games: fields.ReverseRelation["Game"]


class Game(Model):
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat", related_name="games"
    )
    state: GameStates | None = fields.IntEnumField(GameStates, null=True)
    players: fields.ReverseRelation["User"]


class User(Model):
    uid: int = fields.BigIntField()
    role: Roles = fields.CharEnumField(Roles)

    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )
