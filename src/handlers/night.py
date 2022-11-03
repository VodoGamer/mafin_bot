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
    alive_players = await Player.filter(game=game).exclude(role=Role.died)
    for player in active_roles:
        if not player.role:
            raise ValueError(f"WTF! no player role {player.id}")
        await api.send_message(
            player.id,
            f"Ты - {HTMLFormatter(player.role.value).bold()}\nвремя ходить",
            reply_markup=get_players_keyboard(game, alive_players),
            parse_mode=HTMLFormatter.PARSE_MODE,
        )


def get_players_keyboard(game: Game, players: list[Player]) -> InlineKeyboardMarkup:
    KEYBOARD = InlineKeyboard()
    for player in players:
        KEYBOARD.add(InlineButton(player.name, callback_data=f"game/{game.id}/action/{player.id}"))
        KEYBOARD.row()
    return KEYBOARD.get_markup()


@dp.message(State(GameState.night))
async def night(message: Message):
    ...
    # await message.api.delete_message(message.chat.id, message.message_id)
