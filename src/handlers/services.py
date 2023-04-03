from tortoise.expressions import Q

from src.db.models import Game, Life, Player, Role


async def get_active_players(game: Game) -> list[Player]:
    players = await Player.filter(game=game).exclude(Q(role=Role.civilian) | Q(life=Life.died))
    return players


async def get_alive_players(game: Game) -> list[Player]:
    players = await Player.filter(game=game).exclude(life=Life.died)
    return players
