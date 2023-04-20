from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from src.bot.init import db
from src.services import Chat


class GameStatus(Enum):
    enrollment = "Enrollment"
    ended = "Ended"


ADD_CHAT_GAME = open("src/services/queries/add_chat_game.edgeql").read()
GET_GAMES_BY_CHAT_ID = open("src/services/queries/get_games_by_chat_id.edgeql").read()
GET_GAME_BY_UUID = open("src/services/queries/get_game_by_uuid.edgeql").read()


@dataclass(frozen=True, slots=True)
class Game:
    id: UUID
    chat: Chat
    game_status: GameStatus


async def get_last_game(chat_id: int) -> Game | None:
    result = await db.query(GET_GAMES_BY_CHAT_ID, chat_id=chat_id)
    if not result:
        return None
    return result[-1]  # TODO: get by creation date


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
    if game and game.game_status != GameStatus.ended:
        return (game, False)
    game = await create_chat_game(chat_id, chat_title)
    return (game, True)


async def get_game(game_uuid: UUID) -> Game:
    return await db.query_single(GET_GAME_BY_UUID, game_id=game_uuid)
