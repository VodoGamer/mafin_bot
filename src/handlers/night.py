import pathlib

from loguru import logger
from telegrinder import CallbackQuery, Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.types.objects import InlineKeyboardMarkup, InputFile

from src.bot.init import api, formatter
from src.db.models import (
    Action,
    Game,
    GameAction,
    GameMessage,
    GameState,
    MessagePayload,
    Night,
    Player,
    Role,
)
from src.handlers.end import check_for_the_end
from src.handlers.keyboards import get_bot_redirect_kb
from src.handlers.services import get_active_players, get_alive_players
from src.rules import State
from src.templates import render_template

dp = Dispatch()


async def start_night(game: Game):
    if await check_for_the_end(game):
        return
    await Night.create(game=game)
    await api.send_photo(
        chat_id=game.chat_id,
        caption=render_template("night_coming.j2"),
        parse_mode=formatter.PARSE_MODE,
        reply_markup=await get_bot_redirect_kb(),
        photo=InputFile("night.jpg", pathlib.Path("src/images/night.jpg").read_bytes()),
    )

    active_roles = await get_active_players(game)
    logger.debug(f"{active_roles=} now; send action messages for them")
    alive_players = await get_alive_players(game)
    logger.debug(f"{alive_players=} now")

    await api.send_message(
        chat_id=game.chat_id,
        text=render_template("alive_players.j2", {"players": alive_players}),
        parse_mode=formatter.PARSE_MODE,
    )
    for player in active_roles:
        if not player.role:
            raise ValueError(f"WTF! no player role {player.id}")
        result = await api.send_message(
            chat_id=player.id,
            text="Время ходить✊",
            reply_markup=get_players_keyboard(game, player, alive_players),
        )
        await GameMessage.create(
            message_id=result.unwrap().message_id,
            payload=MessagePayload.night_action,
            game=game,
            chat_id=player.id,
        )


def get_players_keyboard(
    game: Game, active_player: Player, players: list[Player]
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    for player in players:
        if player.id == active_player.id and active_player.role in (Role.mafia, Role.don):
            continue
        keyboard.add(InlineButton(player.name, callback_data=f"game/{game.id}/action/{player.id}"))
        keyboard.row()
    return keyboard.get_markup()


@dp.message(State(GameState.night))
async def delete_nights_messages(message: Message):
    await message.api.delete_message(message.chat.id, message.message_id)


async def make_night_action(
    event: CallbackQuery, game_id: int, player_id: int, text: str, action: Action
):
    game = await Game.get(id=game_id)
    player = await Player.get(id=player_id, game=game)
    if event.message:
        await event.api.edit_message_text(
            event.from_user.id,
            event.message.message_id,
            text=f"{text}{player}",
            parse_mode=formatter.PARSE_MODE,
        )
    await GameAction.create(game=game, player=player, type=action)
    return game
