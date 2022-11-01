from datetime import timedelta

from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.bot.rules import Markup, Text
from telegrinder.tools import HTMLFormatter, MarkdownFormatter
from telegrinder.types import InlineKeyboardMarkup

from src.bot.init import api
from src.db.models import Game, GameMessage, GameState, MessagePayload, Player
from src.rules import Command

dp = Dispatch()

START_COMMAND = "/start_set_in_game"
SET_IN_GAME_TIME = timedelta(seconds=60)


@dp.message(Text("/start"))
async def start(message: Message):
    await message.reply(
        f"Для начала игры в {HTMLFormatter('МАФИНЫ').bold()} введите команду {START_COMMAND}",
        parse_mode=HTMLFormatter.PARSE_MODE,
    )


@dp.message(Command(START_COMMAND))
async def set_in_game_command(message: Message):
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
        await start_set_in_game(message, game[0])


async def start_set_in_game(message: Message, game: Game):
    keyboard = await get_set_in_game_keyboard(game)
    result = await message.answer(
        f"{MarkdownFormatter('Набор в игру').bold()}\nЧтобы присоединиться нажми на кнопку ниже",
        parse_mode=MarkdownFormatter.PARSE_MODE,
        reply_markup=keyboard,
    )
    await GameMessage.create(
        game=game,
        message_id=result.unwrap().message_id,
        payload=MessagePayload.set_in_game,
    )


async def get_set_in_game_keyboard(game: Game) -> InlineKeyboardMarkup:
    bot = (await api.get_me()).unwrap()
    KEYBOARD = InlineKeyboard()
    KEYBOARD.add(
        InlineButton("Присоединиться", url=f"https://t.me/{bot.username}?start=join_{game.id}")
    )
    return KEYBOARD.get_markup()


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id)
    player = await Player.get_or_none(id=message.from_user.id).prefetch_related("game")

    if player:
        chat = (await api.get_chat(player.game.chat_id)).unwrap()
        await message.reply(
            f"Ты уже играешь в чате\n{MarkdownFormatter(chat.title).bold()}",
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        return

    chat = (await api.get_chat(game.chat_id)).unwrap()
    await Player.create(id=message.from_user.id, name=message.from_user.first_name, game=game)
    await message.reply(
        f"Ты присоединился к игре {MarkdownFormatter(chat.title).bold()}",
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )
    await update_set_in_game_message(game)


async def update_set_in_game_message(game: Game):
    chat_message = await GameMessage.get(game=game, payload=MessagePayload.set_in_game)
    keyboard = await get_set_in_game_keyboard(game)
    players = map(str, await Player.filter(game=game))

    await api.edit_message_text(
        chat_id=game.chat_id,
        message_id=chat_message.message_id,
        text=f"{MarkdownFormatter('Набор в игру').bold()}\nУчаствуют:\n{', '.join(players)}",
        reply_markup=keyboard,
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )


async def send_or_update_timer(game: Game, seconds: int):
    text = MarkdownFormatter("До начала игры").bold() + " осталось {} секунд"

    timer = await GameMessage.get_or_none(game=game, payload=MessagePayload.timer)
    if timer:
        await api.edit_message_text(
            game.chat_id,
            timer.message_id,
            text=text.format(seconds),
            parse_mode=MarkdownFormatter.PARSE_MODE,
        )
        return
    message = await api.send_message(
        game.chat_id, text.format(seconds), parse_mode=MarkdownFormatter.PARSE_MODE
    )
    await GameMessage.create(
        game=game, payload=MessagePayload.timer, message_id=message.unwrap().message_id
    )
