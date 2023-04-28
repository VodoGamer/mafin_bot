from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from src.bot.init import db
from src.services import Chat, Game
from src.services.abc import read_query


class MessagePayload(Enum):
    enrollment = "Enrollment"
    timer = "Timer"


@dataclass(frozen=True, slots=True)
class GameMessage:
    id: UUID
    message_id: int
    message_payload: MessagePayload

    game: Game
    chat: Chat


ADD_MESSAGE = read_query("add_message.edgeql")
GET_MESSAGE = read_query("get_message.edgeql")


async def create_message(
    message_id: int, message_payload: MessagePayload, chat_id: int, game_uuid: UUID
) -> GameMessage:
    return await db.query_single(
        ADD_MESSAGE,
        message_id=message_id,
        message_payload=message_payload.value,
        chat_id=chat_id,
        game_uuid=game_uuid,
    )


async def get_message(chat_id: int, message_payload: MessagePayload) -> GameMessage | None:
    result = await db.query(GET_MESSAGE, chat_id=chat_id, message_payload=message_payload.value)
    if not result:
        return None
    return result[0]
