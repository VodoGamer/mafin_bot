from loguru import logger
from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataMarkup
from telegrinder.tools import MarkdownFormatter
from tortoise.functions import Count

from src.bot.init import api
from src.db.models import Game, GameAction, GameMessage, GameState, Life, Player, Vote
from src.handlers.night import start_night

dp = Dispatch()


@dp.callback_query(CallbackDataMarkup("game/<game_id>/vote/<player_id>"))
async def vote(event: CallbackQuery, game_id: int, player_id: int):
    if not event.message:
        return
    game = await Game.get(id=game_id)
    player = await Player.get(id=player_id, game=game)
    from_player = await Player.get(id=event.from_user.id, game=game)
    await api.edit_message_text(
        event.from_user.id,
        event.message.message_id,
        text=f"ты проголосовал за: {str(player)}",
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
    await Vote.create(game_id=game_id, goal_user=player)
    await api.send_message(
        game.chat_id, f"{from_player} проголосовал за кик", parse_mode=MarkdownFormatter.PARSE_MODE
    )
    if await check_for_end_voting(game):
        await end_day(game)


async def end_day(game: Game):
    messages = await GameMessage.filter(game=game)
    for message in messages:
        await api.delete_message(message.chat_id, message.message_id)
    await end_voting(game)
    game.state = GameState.night
    await game.save()
    await GameAction.filter(game=game).delete()
    await Vote.filter(game=game).delete()
    await start_night(game)


async def check_for_end_voting(game: Game):
    votes = await Vote.filter(game=game).count()
    players = await Player.filter(game=game).exclude(life=Life.died).count()
    return votes == players


async def end_voting(game: Game):
    most_votes = (
        await Vote.annotate(count=Count("id"))
        .group_by("goal_user_id")
        .order_by("-count")
        .values_list("goal_user_id", "count")
    )
    logger.debug(f"{most_votes=}")
    if not most_votes or (len(most_votes) > 1 and most_votes[0][1] == most_votes[1][1]):
        await api.send_message(game.chat_id, "жители не определились")
    else:
        player = await Player.get(game=game, id=most_votes[0][0])
        player.life = Life.died
        await player.save()
        await api.send_message(
            game.chat_id, f"вешаем {player}", parse_mode=MarkdownFormatter.PARSE_MODE
        )
