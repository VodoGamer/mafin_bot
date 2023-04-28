"""start and process enrollment in the game"""
from uuid import UUID

from telegrinder import Dispatch, Message

from src.bot.init import api, formatter
from src.handlers.keyboards import get_join_game_kb
from src.handlers.timers import TIMER_DURATION, send_timer_message, start_timer_poling
from src.rules import ChatCommand
from src.services import MessagePayload, Player, create_message, init_enrollment
from src.templates import render_template

dp = Dispatch()


@dp.message(ChatCommand("/enrollment"))
async def start_enrollment_in_chat(message: Message):
    game = await init_enrollment(message.chat.id, message.chat.title)
    if not game[1]:
        await message.delete()
        return

    bot = (await api.get_me()).unwrap()
    output_message = (
        await message.answer(
            render_template("enrollment.j2"),
            parse_mode=formatter.PARSE_MODE,
            reply_markup=get_join_game_kb(game[0].id, bot.username),
        )
    ).unwrap()
    await api.pin_chat_message(
        chat_id=message.chat.id, message_id=output_message.message_id, disable_notification=True
    )
    await create_message(
        output_message.message_id, MessagePayload.enrollment, message.chat.id, game[0].id
    )

    await send_timer_message(message.chat.id, TIMER_DURATION)
    start_timer_poling(message.chat.id)


async def update_enrollment_message(
    chat_id: int, game_id: UUID, message_id: int, players: list[Player]
):
    bot = (await api.get_me()).unwrap()
    await api.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=render_template("enrollment.j2", {"players": players}),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=get_join_game_kb(game_id, bot.username),
    )
