"""start and process enrollment in the game"""
from telegrinder import Dispatch, Message
from telegrinder.rules import Markup

from src.bot.init import formatter
from src.db.models import Chat, Game, GameMessage, MessagePayload, Player
from src.handlers.enrollment import update_enrollment_message
from src.templates import render_template

dp = Dispatch()


@dp.message(Markup("/start join_<game_id>"))
async def join_game(message: Message, game_id: int):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"

    game = await Game.get(id=game_id).prefetch_related("chat")
    player = await Player.get_or_create({"game": game, "name": full_name}, id=message.from_user.id)

    if not player[1]:
        chat = await Chat.get(games__players__id=player[0].id)
        await message.answer(
            render_template("already_in_game.j2", {"chat": chat}),
            formatter=formatter.PARSE_MODE,
        )
        return
    await message.answer(render_template("joined_in_game.j2"), formatter=formatter.PARSE_MODE)

    enrollment_message = await GameMessage.get(game=game, payload=MessagePayload.enrollment)
    all_players = await Player.filter(game=game)
    await update_enrollment_message(game.chat.id, game.id, enrollment_message.id, all_players)
