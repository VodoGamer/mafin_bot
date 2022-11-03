from telegrinder import CallbackQuery, Dispatch
from telegrinder.rules import CallbackDataMarkup
from telegrinder.tools import MarkdownFormatter
from tortoise.functions import Count

from src.bot.init import api
from src.db.models import Game, Player, Role, Vote

dp = Dispatch()


@dp.callback_query(CallbackDataMarkup("game/<game_id>/vote/<player_id>"))
async def vote(event: CallbackQuery, game_id: int, player_id: int):
    if not event.message:
        return
    player = await Player.get(id=player_id).prefetch_related("game")
    await api.edit_message_text(
        event.from_user.id,
        event.message.message_id,
        text=f"u choice {str(player)}",
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
    await Vote.create(game=player.game, goal_user=player)
    await check_for_end_voting(player.game)


async def check_for_end_voting(game: Game):
    votes = await Vote.filter(game=game).count()
    players = await Player.filter(game=game).exclude(role=Role.died).count()
    if votes != players:
        return
    most_votes = (
        await Vote.annotate(count=Count("id"))
        .group_by("goal_user_id")
        .order_by("-count")
        .values_list("goal_user_id", "count")
    )
    if most_votes[0][1] == most_votes[1][1]:
        await api.send_message(game.chat_id, "жители не определились")
        return
    player = await Player.get(game=game, id=most_votes[0][0])
    await api.send_message(game.chat_id, f"{player} <- этого лоха повесили ХАВХАВХАВХВАХ")
