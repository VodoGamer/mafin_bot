from enum import Enum

from tortoise import fields
from tortoise.models import Model


class Chat(Model):
    id = fields.BigIntField(pk=True)
    title = fields.CharField(255)

    # relations
    games: fields.ReverseRelation["Game"]

    class Meta:
        table = "chat"


class GameStates(Enum):
    enrollment = "enrollment in game"


class Game(Model):
    id = fields.IntField(pk=True)
    state = fields.CharEnumField(GameStates)

    # relations
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat", related_name="games"
    )
    messages: fields.ReverseRelation["GameMessage"]
    players: fields.ReverseRelation["Player"]

    class Meta:
        table = "game"


class MessagePayload(Enum):
    enrollment = "enrollment in game message"


class GameMessage(Model):
    id = fields.IntField(pk=True)
    message_id = fields.IntField()
    payload = fields.CharEnumField(MessagePayload)

    # relations
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="messages"
    )

    class Meta:
        table = "game_message"


class Player(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(255)

    # relations
    game: fields.ForeignKeyRelation[Game] = fields.ForeignKeyField(
        "models.Game", related_name="players"
    )

    class Meta:
        table = "player"
