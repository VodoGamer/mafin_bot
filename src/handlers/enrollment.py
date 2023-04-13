"""start and process enrollment in the game"""
from telegrinder import Dispatch, Message
from telegrinder.rules import Markup

from src.bot.init import api, formatter
from src.db.models import Chat, Game, GameMessage, GameStates, MessagePayload, Player
from src.handlers.keyboards import get_enrollment_kb
from src.rules import ChatCommand
from src.templates import render_template

dp = Dispatch()


@dp.message(ChatCommand("/enrollment"))
async def start_enrollment_in_chat(message: Message):
    chat = await Chat.get_or_create({"title": message.chat.title}, id=message.chat.id)
    game = await Game.get_or_create({"state": GameStates.enrollment}, chat=chat[0])
    if not game[1]:
        await message.delete()
        return

    bot = (await api.get_me()).unwrap()
    output_message = (
        await message.answer(
            render_template("enrollment.j2"),
            parse_mode=formatter.PARSE_MODE,
            reply_markup=get_enrollment_kb(game[0].id, bot.username),
        )
    ).unwrap()
    await api.pin_chat_message(
        chat_id=chat[0].id,
        message_id=output_message.message_id,
        disable_notification=True,
    )

    await GameMessage.create(
        game=game[0],
        message_id=output_message.message_id,
        payload=MessagePayload.enrollment,
    )


async def update_enrollment_message(
    chat_id: int, game_id: int, message_id: int, players: list[Player]
):
    bot = (await api.get_me()).unwrap()
    await api.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=render_template("enrollment.j2", {"players": players}),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=get_enrollment_kb(game_id, bot.username),
    )
