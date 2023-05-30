from telegrinder import Dispatch, Message

from src.bot.init import api
from src.handlers.end_game import check_for_end_game, end_game
from src.rules.game_state import GameStatusRule
from src.services.game import Game, GameStatus, change_game_status
from src.services.player import get_all_players

dp = Dispatch()


async def start_night(game: Game):
    players = await get_all_players(game.id)
    if await check_for_end_game(players):
        await end_game(game, "Игра окончена")
        return None
    await api.send_message(game.chat.chat_id, text="Наступает ночь!")
    await change_game_status(game.id, GameStatus.night)


@dp.message(GameStatusRule(GameStatus.night))
async def night_message(message: Message):
    await message.delete()
