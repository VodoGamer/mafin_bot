from src.bot.init import api
from src.services import Game, Player, PlayerRole
from src.services.game import GameStatus, change_game_status


async def check_for_end_game(players: list[Player]) -> bool:
    civilian_count = 0
    mafia_count = 0
    for player in players:
        if player.role == PlayerRole.Civilian:
            civilian_count += 1
        elif player.role == PlayerRole.Mafia:
            mafia_count += 1
    if mafia_count >= civilian_count:
        return False
    return True


async def end_game(game: Game, message: str):
    await api.send_message(game.chat.chat_id, text=message)
    await change_game_status(game.id, GameStatus.ended)
