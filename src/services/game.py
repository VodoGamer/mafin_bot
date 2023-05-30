from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

from src.bot.init import db
from src.services import Chat
from src.services.abc import read_query


class GameStatus(Enum):
    enrollment = "Enrollment"
    role_assignment = "RoleAssignment"
    ended = "Ended"


@dataclass(frozen=True, slots=True)
class Game:
    id: UUID
    chat: Chat
    start_date: datetime
    status: GameStatus


ADD_CHAT_GAME = read_query("add_chat_game.edgeql")
GET_GAMES_BY_CHAT_ID = read_query("get_games_by_chat_id.edgeql")
GET_GAME_BY_UUID = read_query("get_game_by_uuid.edgeql")
GET_ALL_ENROLLMENT_GAMES = read_query("get_all_enrollment_games.edgeql")
UPDATE_GAME_STATUS = read_query("update_game_status.edgeql")


async def get_last_game(chat_id: int) -> Game | None:
    result = await db.query(GET_GAMES_BY_CHAT_ID, chat_id=chat_id)
    if not result:
        return None
    return result[-1]


async def create_chat_game(chat_id: int, chat_title: str | None = "test") -> Game:
    return await db.query_single(ADD_CHAT_GAME, chat_id=chat_id, title=chat_title)


async def init_enrollment(chat_id: int, chat_title: str | None = "test") -> tuple[Game, bool]:
    """Initializes a new game

    Args:
        chat_id (int): chat_id
        chat_title (str | None, optional): chat title. Defaults to "test".

    Returns:
        tuple[Game, bool]: return bool as True if the game created,
        return False if game already existed
    """
    game = await get_last_game(chat_id)
    if game and game.status != GameStatus.ended:
        return (game, False)
    game = await create_chat_game(chat_id, chat_title)
    return (game, True)


async def get_game(game_uuid: UUID) -> Game:
    return await db.query_single(GET_GAME_BY_UUID, game_id=game_uuid)


async def get_enrollment_games() -> list[Game] | None:
    return await db.query(GET_ALL_ENROLLMENT_GAMES)


async def change_game_status(game_uuid: UUID, new_status: GameStatus):
    await db.query(UPDATE_GAME_STATUS, game_id=game_uuid, status=new_status.value)
