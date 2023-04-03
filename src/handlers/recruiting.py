from datetime import timedelta

from telegrinder import Dispatch, Message
from telegrinder.bot.rules import Markup

from src.bot.init import api, formatter
from src.db.models import Game, GameMessage, GameState, MessagePayload, Player
from src.handlers.keyboards import get_join_game_kb
from src.handlers.timer import check_game_timers
from src.rules import ChatCommand
from src.templates import render_template

dp = Dispatch()


@dp.message(ChatCommand("/start"))
async def start(message: Message):
    await message.reply(render_template("start.j2"), parse_mode=formatter.PARSE_MODE)


@dp.message(ChatCommand("/recruiting"))
async def recruiting(message: Message):
    game = await Game.get_or_create(
        {
            "state": GameState.recruiting,
        },
        chat_id=message.chat.id,
    )
    if game[1]:
        await start_recruiting(game[0])


@dp.message(ChatCommand("/expand_time"))
async def expand_time(message: Message):
    added_time = timedelta(seconds=20)
    game = await Game.get_or_none(chat_id=message.chat.id, state=GameState.recruiting)
    if game:
        game.start_date += added_time
        await game.save()
        await message.answer(render_template("added_time.j2", {"time": added_time.seconds}))
        await check_game_timers(game)


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id)
    player = await Player.get_or_none(id=message.from_user.id).prefetch_related("game")

    if player:
        side_chat = (await api.get_chat(player.game.chat_id)).unwrap()
        await message.reply(
            render_template("user_already_play.j2", {"chat": side_chat}),
            parse_mode=formatter.PARSE_MODE,
        )
        return

    chat = (await api.get_chat(game.chat_id)).unwrap()
    await Player.create(id=message.from_user.id, name=message.from_user.first_name, game=game)
    await message.reply(
        render_template("user_already_play.j2", {"chat": chat}), parse_mode=formatter.PARSE_MODE
    )
    await update_recruiting_message(game)


async def start_recruiting(game: Game):
    me = (await api.get_me()).unwrap()
    message = (
        await api.send_message(
            chat_id=game.chat_id,
            text=render_template("recruiting.j2"),
            parse_mode=formatter.PARSE_MODE,
            reply_markup=await get_join_game_kb(me.username, game.id),
        )
    ).unwrap()
    await api.pin_chat_message(game.chat_id, message.message_id, disable_notification=True)
    await GameMessage.create(
        game=game, message_id=message.message_id, payload=MessagePayload.recruiting
    )


async def update_recruiting_message(game: Game):
    message = await GameMessage.get(game=game, payload=MessagePayload.recruiting)
    players = await Player.filter(game=game)

    me = (await api.get_me()).unwrap()
    message = await api.edit_message_text(
        chat_id=game.chat_id,
        message_id=message.message_id,
        text=render_template("recruiting.j2", {"players": players}),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=await get_join_game_kb(me.username, game.id),
    )
