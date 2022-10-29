from datetime import timedelta

from telegrinder import API, Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.bot.rules import Markup, Text
from telegrinder.tools import MarkdownFormatter
from telegrinder.types import User

from src.db.models import Game, GameMessage, GameState, MessagePayload, Player
from src.handlers.start import start_timer_to_the_game
from src.rules import Command

dp = Dispatch()

START_COMMAND = "/start_mafin"


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(f"start placeholder\nдля начала игры введите команду \n{START_COMMAND}")


@dp.message(Command(START_COMMAND))
async def start_set_in_game(message: Message):
    await message.api.delete_message(message.chat.id, message.message_id)
    if message.chat.type == "private":
        await message.reply("Игры в мафины доступны только в чате")
        return

    game = await Game.get_or_create({"state": GameState.set_in_game}, chat_id=message.chat.id)
    if game[1]:
        bot = (await message.api.get_me()).unwrap()

        result = await message.answer(
            "set a game placeholder",
            reply_markup=get_set_in_game_keyboard(bot, game[0]).get_markup(),
        )
        await GameMessage.create(
            game=game[0],
            message_id=result.unwrap().message_id,
            payload=MessagePayload.set_in_game,
        )
        await start_timer_to_the_game(timedelta(seconds=30), game[0])


def get_set_in_game_keyboard(bot: User, game: Game) -> InlineKeyboard:
    KEYBOARD = InlineKeyboard()
    KEYBOARD.add(
        InlineButton("join placeholder", url=f"https://t.me/{bot.username}?start=join_{game.id}")
    )
    return KEYBOARD


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id)
    player = await Player.get_or_none(id=message.from_user.id)
    chat = (await message.api.get_chat(game.chat_id)).unwrap()

    if player:
        await message.reply(f"alredy in game placeholder {chat.title}")
        return
    await Player.create(id=message.from_user.id, name=message.from_user.first_name, game=game)
    await message.reply(f"join game placeholder {chat.title}")
    await update_players_list(message.api, game)


async def update_players_list(api: API, game: Game):
    chat_message = await GameMessage.get(game=game, payload=MessagePayload.set_in_game)
    players = map(str, await Player.filter(game=game))
    me = (await api.get_me()).unwrap()
    await api.edit_message_text(
        game.chat_id,
        chat_message.message_id,
        text=f"set a game placeholder\n{', '.join(players)}",
        reply_markup=get_set_in_game_keyboard(me, game).get_markup(),
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
