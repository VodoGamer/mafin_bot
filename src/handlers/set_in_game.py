from datetime import timedelta

from loguru import logger
from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.bot.rules import Markup
from telegrinder.tools import MarkdownFormatter
from telegrinder.types import InlineKeyboardMarkup

from src.bot.init import api
from src.bot.phrases import set_game_0_players, set_game_with_players, start_command
from src.db.models import Game, GameMessage, GameState, MessagePayload, Player
from src.rules import ChatCommand

dp = Dispatch()

START_COMMAND = "/set_in_game"
SET_IN_GAME_TIME = timedelta(seconds=60)


@dp.message(ChatCommand("/start"))
async def start(message: Message):
    await message.reply(start_command.text, parse_mode=start_command.PARSE_MODE)


@dp.message(ChatCommand(START_COMMAND))
async def set_in_game_command(message: Message):
    await api.delete_message(message.chat.id, message.message_id)
    game = await Game.get_or_create(
        {
            "state": GameState.set_in_game,
        },
        chat_id=message.chat.id,
    )
    logger.debug(f"{game[0].chat_id} | {game=}")
    if game[1]:
        await set_in_game(game[0])


async def set_in_game(game: Game):
    keyboard = await get_set_in_game_markup(game)
    message = (
        await api.send_message(
            chat_id=game.chat_id,
            text=set_game_0_players.text,
            parse_mode=set_game_0_players.PARSE_MODE,
            reply_markup=keyboard,
        )
    ).unwrap()
    await api.pin_chat_message(game.chat_id, message.message_id, disable_notification=True)
    await GameMessage.create(
        game=game,
        message_id=message.message_id,
        payload=MessagePayload.set_in_game,
    )


async def get_set_in_game_markup(game: Game) -> InlineKeyboardMarkup:
    bot = (await api.get_me()).unwrap()
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Присоединиться", url=f"https://t.me/{bot.username}?start=join_{game.id}")
    )
    return keyboard.get_markup()


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id)
    player = await Player.get_or_none(id=message.from_user.id).prefetch_related("game")
    logger.debug(f"from {message.from_user.id} to {game=} | {player=}")

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
    logger.debug(f"{message.from_user.id} successfully join in the {game=}")
    await update_set_in_game_message(game)


async def update_set_in_game_message(game: Game):
    message = await GameMessage.get(game=game, payload=MessagePayload.set_in_game)
    keyboard = await get_set_in_game_markup(game)
    players = await Player.filter(game=game)
    logger.debug(f"{game=} players now: {players}")

    message = await api.edit_message_text(
        chat_id=game.chat_id,
        message_id=message.message_id,
        text=set_game_with_players.text.format(
            players=", ".join(map(str, players)), players_count=len(players)
        ),
        reply_markup=keyboard,
        parse_mode=set_game_with_players.PARSE_MODE,
    )
