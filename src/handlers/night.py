from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.tools import HTMLFormatter
from telegrinder.types.objects import InlineKeyboardMarkup

from src.bot.init import api
from src.db.models import Game, GameState, Player, Role
from src.rules import State

dp = Dispatch()


async def start_night(game: Game):
    active_roles = await Player.filter(game=game).exclude(role=Role.civilian)
    for player in active_roles:
        if not player.role:
            raise ValueError(f"WTF! no player role {player.id}")
        await api.send_message(
            player.id,
            f"Ты - {HTMLFormatter(player.role.value).bold()}\nвремя ходить",
            reply_markup=get_players_keyboard(game, game.players),
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
