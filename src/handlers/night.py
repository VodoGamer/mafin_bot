from telegrinder import Dispatch, InlineButton, InlineKeyboard, Message
from telegrinder.types.objects import InlineKeyboardMarkup


from src.bot.init import api
from src.db.models import Game, GameState, Player, Role
from src.rules import State

dp = Dispatch()


async def start_night(game: Game):
    active_roles = await Player.filter(game=game).exclude(role=Role.civilian)
    for player in active_roles:
        await api.send_message(
            player.id, "action placeholder", reply_markup=get_players_keyboard(game, game.players)
        )


def get_players_keyboard(game: Game, players: list[Player]) -> InlineKeyboardMarkup:
    KEYBOARD = InlineKeyboard()
    for player in players:
        KEYBOARD.add(
            InlineButton(player.username, callback_data=f"game/{game.id}/action/{player.id}")
        )
        KEYBOARD.row()
    return KEYBOARD.get_markup()


@dp.message(State(GameState.night))
async def night(message: Message):
    ...
    # await message.api.delete_message(message.chat.id, message.message_id)
