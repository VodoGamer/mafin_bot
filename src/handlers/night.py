from loguru import logger
from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.tools import HTMLFormatter, MarkdownFormatter
from telegrinder.types.objects import InlineKeyboardMarkup
from tortoise.expressions import Q

from src.bot.init import api
from src.db.models import Game, GameState, Player, Role
from src.handlers.end import check_for_the_end
from src.rules import State

dp = Dispatch()


async def start_night(game: Game):
    if await check_for_the_end(game):
        return
    await api.send_message(
        game.chat_id,
        MarkdownFormatter("НАСТУПАЕТ НОЧЬ").bold(),
        parse_mode=MarkdownFormatter.PARSE_MODE,
    )

    active_roles = await Player.filter(game=game).exclude(
        Q(role=Role.civilian) | Q(role=Role.died)
    )
    logger.debug(f"{active_roles=} now; send action messages for them")
    alive_players = await Player.filter(game=game).exclude(role=Role.died)
    logger.debug(f"{alive_players=} now")
    for player in active_roles:
        if not player.role:
            raise ValueError(f"WTF! no player role {player.id}")
        await api.send_message(
            player.id,
            f"Ты - {HTMLFormatter(player.role.value).bold()}\nвремя ходить",
            reply_markup=get_players_keyboard(game, player, alive_players),
            parse_mode=HTMLFormatter.PARSE_MODE,
        )


def get_players_keyboard(
    game: Game, active_player: Player, players: list[Player]
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    for player in players:
        if active_player.role == Role.mafia and player.id == active_player.id:
            continue
        keyboard.add(InlineButton(player.name, callback_data=f"game/{game.id}/action/{player.id}"))
        keyboard.row()
    return keyboard.get_markup()


@dp.message(State(GameState.night))
async def delete_nights_messages(message: Message):
    await message.api.delete_message(message.chat.id, message.message_id)
