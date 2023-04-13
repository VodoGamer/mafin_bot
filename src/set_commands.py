from telegrinder import API, Token
from telegrinder.types import BotCommand

from src.config.env import BOT_TOKEN

api = API(token=Token(BOT_TOKEN))


commands_list = [
    BotCommand(command="/start", description="Начало бота").to_dict(),
]


async def update_bot_settings_list():
    await api.delete_my_commands()
    await api.set_my_commands(
        commands_list,  # type: ignore
    )
