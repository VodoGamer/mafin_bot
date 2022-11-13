from loguru import logger
from telegrinder import Dispatch
from telegrinder.tools import MarkdownFormatter

from src.bot.init import api
from src.db.models import Game, Life, Player, Role

dp = Dispatch()


async def check_for_the_end(game: Game):
    alive_players = await Player.filter(game=game).exclude(life=Life.died).count()
    all_players = [
        f"{MarkdownFormatter(player.name).mention(player.id)} – {player.role.value}"
        for player in await Player.filter(game=game)
    ]
    mafia = await Player.filter(game=game, role=Role.mafia).exclude(life=Life.died).count()
    logger.debug(f"{alive_players=} and {mafia=} alive now")
    if mafia <= 0:
        await api.send_message(
            game.chat_id,
            "ИГРА ОКОНЧЕНА\nПобедили мирные\n\n{}".format("\n".join(all_players)),
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        await game.delete()
        return True
    if alive_players <= mafia * 2:
        await api.send_message(
            game.chat_id,
            "ИГРА ОКОНЧЕНА\nПобедила мафия\n\n{}".format("\n".join(all_players)),
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        await game.delete()
        return True
