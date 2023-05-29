import random
from uuid import UUID

from src.bot.init import api
from src.handlers.end_game import check_for_end_game
from src.services import Player, PlayerRole, get_all_players, update_player_role
from src.services.game import get_game


async def start_game(game_uuid: UUID) -> None:
    players = await get_all_players(game_uuid)
    if not await _check_for_start_game(players):
        game = await get_game(game_uuid)
        await api.send_message(game.chat.chat_id, text="Никто не пришёл на сходку(")
        return None
    await _set_random_player_to_role(players, PlayerRole.Mafia)


async def _check_for_start_game(players: list[Player]) -> bool:
    if len(players) <= 3:
        return False
    return True


async def _set_random_player_to_role(players: list[Player], role: PlayerRole) -> None:
    mafia_player = _pop_random_player(players)
    await update_player_role(mafia_player.user_id, role)


def _pop_random_player(players: list[Player]) -> Player:
    return players.pop(random.randint(1, len(players)) - 1)
