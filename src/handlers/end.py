from loguru import logger
from tortoise.expressions import Q

from src.bot.init import api, formatter
from src.db.models import Game, Life, Player, Role
from src.handlers.services import get_alive_players
from src.templates import render_template


async def check_for_the_end(game: Game):
    alive_players_count = len(await get_alive_players(game))
    all_players = await Player.filter(game=game)
    alive_mafia_count = await Player.filter(
        Q(game=game) & (Q(role=Role.mafia) | Q(role=Role.don)) & ~Q(life=Life.died)
    ).count()
    logger.debug(f"{alive_players_count=} and {alive_mafia_count=} now")
    if alive_mafia_count <= 0:
        output_text = render_template(
            "game_over.j2", {"winner": "civilians", "players": all_players}
        )
    elif alive_players_count <= alive_mafia_count * 2:
        output_text = render_template("game_over.j2", {"winner": "mafia", "players": all_players})
    else:
        return False
    await api.send_message(
        chat_id=game.chat_id,
        text=output_text,
        parse_mode=formatter.PARSE_MODE,
    )
    await game.delete()
    return True
