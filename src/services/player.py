from dataclasses import dataclass
from uuid import UUID

from src.bot.init import db
from src.services import Chat, Game
from src.services.abc import read_query


@dataclass(frozen=True, slots=True)
class Player:
    user_id: int
    name: str

    game: Game
    chat: Chat


GET_PLAYER_BY_ID = read_query("src/services/queries/get_player_by_id.edgeql")
ADD_GAME_PLAYER = read_query("src/services/queries/add_game_player.edgeql")
GET_ALL_PLAYERS = read_query("src/services/queries/get_all_players.edgeql")


async def get_player(user_id: int) -> Player | None:
    result = await db.query(GET_PLAYER_BY_ID, user_id=user_id)
    if not result:
        return None
    return result[0]


async def create_player(user_id: int, user_name: str, chat_id: int, game_uuid: UUID) -> Player:
    return await db.query_single(
        ADD_GAME_PLAYER, user_id=user_id, name=user_name, chat_id=chat_id, game_id=game_uuid
    )


async def init_game_player(
    user_id: int, user_name: str, chat_id: int, game_uuid: UUID
) -> tuple[Player, bool]:
    player = await get_player(user_id)
    if player:
        return (player, False)
    player = await create_player(user_id, user_name, chat_id, game_uuid)
    return (player, True)


async def get_all_players(game_uuid: UUID) -> list[Player]:
    return await db.query(GET_ALL_PLAYERS, game_id=game_uuid)
