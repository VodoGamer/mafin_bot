import random

from src.bot.init import api
from src.handlers.night import start_night
from src.services import Game, Player, PlayerRole, get_all_players, update_player_role
from src.services.game import GameStatus, change_game_status


async def start_game(game: Game) -> None:
    await change_game_status(game.id, GameStatus.role_assignment)
    players = await get_all_players(game.id)
    if not await _check_for_start_game(players):
        await api.send_message(game.chat.chat_id, text="Никто не пришёл на сходку(")
        await change_game_status(game.id, GameStatus.ended)
        return None
    await _set_random_player_to_role(players, PlayerRole.Mafia)
    await api.send_message(game.chat.chat_id, text="Игра начинается!")
    await start_night(game)


async def _check_for_start_game(players: list[Player]) -> bool:
    if len(players) <= 3:
        return False
    return True


async def _set_random_player_to_role(players: list[Player], role: PlayerRole) -> None:
    mafia_player = _pop_random_player(players)
    await update_player_role(mafia_player.user_id, role)


def _pop_random_player(players: list[Player]) -> Player:
    return players.pop(random.randint(1, len(players)) - 1)
