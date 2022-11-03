from loguru import logger
from telegrinder import Dispatch

from src.bot.init import api
from src.db.models import Game, Player, Role

dp = Dispatch()


async def check_for_the_end(game: Game):
    logger.debug("start check fot the ends game")
    players = await Player.filter(game=game).exclude(role=Role.died).count()
    mafia = await Player.filter(game=game, role=Role.mafia).count()
    logger.debug(f"{players} alive and {mafia} mafias now")
    if mafia <= 0:
        await api.send_message(game.chat_id, "ИГРА ОКОНЧЕНА\nПобедили мирные")
        await game.delete()
        return True
    if players <= mafia * 2:
        await api.send_message(game.chat_id, "ИГРА ОКОНЧЕНА\nПобедила мафия")
        await game.delete()
        return True
