from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataMarkup

from src.bot.init import api
from src.db.models import Game, Player, Vote

dp = Dispatch()


@dp.callback_query(CallbackDataMarkup("game/<game_id>/vote/<player_id>"))
async def vote(event: CallbackQuery, game_id: int, player_id: int):
    game = await Game.get(id=game_id)
    if not event.message:
        return
    await api.edit_message_text(
        event.from_user.id, event.message.message_id, text=f"u choice {player_id}"
    )
    await Vote.create(game=game, goal_user_id=player_id)
    await check_for_end_voting(game)


async def check_for_end_voting(game: Game):
    votes = await Vote.filter(game=game)
    alive_players = await Player.filter(game=game)
    if len(votes) == len(alive_players):
        await api.send_message(game.chat_id, "")
