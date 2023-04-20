"""start and process enrollment in the game"""
from uuid import UUID

from telegrinder import Dispatch, Message
from telegrinder.rules import Markup

from src.bot.init import formatter
from src.services import get_game, init_game_player
from src.templates import render_template

dp = Dispatch()


@dp.message(Markup("/start join_<game_uuid>"))
async def join_game(message: Message, game_uuid: UUID):
    game = await get_game(game_uuid)
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"

    player = await init_game_player(message.from_user.id, full_name, game.chat.chat_id, game_uuid)
    if not player[1]:
        await message.answer(
            render_template("already_in_game.j2", {"chat": player[0].chat}),
            formatter=formatter.PARSE_MODE,
        )
        return
    await message.answer(render_template("joined_in_game.j2"), formatter=formatter.PARSE_MODE)

    # all_players = await get_all_players(game_uuid)
    # TODO: await update_enrollment_message
