from src.services import Player
from src.services.player import PlayerRole


async def check_for_end_game(players: list[Player]) -> bool:
    civilian_count = 0
    mafia_count = 0
    for player in players:
        if player.role == PlayerRole.Civilian:
            civilian_count += 1
        elif player.role == PlayerRole.Mafia:
            mafia_count += 1
    if mafia_count >= civilian_count + 1:
        return False
    return True
