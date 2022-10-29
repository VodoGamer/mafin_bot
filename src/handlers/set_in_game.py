from datetime import timedelta

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.bot.rules import Markup, Text
from telegrinder.tools import MarkdownFormatter
from telegrinder.types import InlineKeyboardMarkup

from src.bot.init import api
from src.db.models import Game, GameMessage, GameState, MessagePayload, Player
from src.rules import Command

dp = Dispatch()

START_COMMAND = "/start_set_in_game"
SET_IN_GAME_TIME = timedelta(seconds=60)


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(f"start placeholder\nдля начала игры введите команду \n{START_COMMAND}")


@dp.message(Command(START_COMMAND))
async def start_set_in_game(message: Message):
    await api.delete_message(message.chat.id, message.message_id)
    if message.chat.type == "private":
        await message.reply("Игры в мафины доступны только в чате")
        return

    game = await Game.get_or_create(
        {
            "state": GameState.set_in_game,
        },
        chat_id=message.chat.id,
    )
    if game[1]:
        await send_set_in_game_message(message, game[0])


async def send_set_in_game_message(message: Message, game: Game):
    keyboard = await get_set_in_game_keyboard(game)
    result = await message.answer("set a game placeholder", reply_markup=keyboard)
    await GameMessage.create(
        game=game,
        message_id=result.unwrap().message_id,
        payload=MessagePayload.set_in_game,
    )


async def get_set_in_game_keyboard(game: Game) -> InlineKeyboardMarkup:
    bot = (await api.get_me()).unwrap()
    KEYBOARD = InlineKeyboard()
    KEYBOARD.add(
        InlineButton("join placeholder", url=f"https://t.me/{bot.username}?start=join_{game.id}")
    )
    return KEYBOARD.get_markup()


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id)
    player = await Player.get_or_none(id=message.from_user.id)
    chat = (await api.get_chat(game.chat_id)).unwrap()

    if player:
        await message.reply(f"alredy in game placeholder {chat.title}")
        return
    await Player.create(id=message.from_user.id, name=message.from_user.first_name, game=game)
    await message.reply(f"join game placeholder {chat.title}")
    await update_set_in_game_message(game)


async def update_set_in_game_message(game: Game):
    chat_message = await GameMessage.get(game=game, payload=MessagePayload.set_in_game)
    keyboard = await get_set_in_game_keyboard(game)
    players = map(str, await Player.filter(game=game))

    await api.edit_message_text(
        chat_id=game.chat_id,
        message_id=chat_message.message_id,
        text=f"set a game placeholder:\n{', '.join(players)}",
        reply_markup=keyboard,
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )


async def send_or_update_timer(game: Game, seconds: int):
    text = "before the game: {} placeholder"

    timer = await GameMessage.get_or_none(game=game, payload=MessagePayload.timer)
    if timer:
        await api.edit_message_text(game.chat_id, timer.message_id, text=text.format(seconds))
        return
    message = await api.send_message(game.chat_id, text.format(seconds))
    await GameMessage.create(
        game=game, payload=MessagePayload.timer, message_id=message.unwrap().message_id
    )
