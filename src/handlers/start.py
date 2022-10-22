from telegrinder import Dispatch, Message, InlineKeyboard, InlineButton
from telegrinder.bot.rules import Text, Markup
from src.db.models import Chat, Game, GameState, Player

from src.rules.command import Command

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
    chat = await Chat.get_or_create(id=message.chat.id)
    game = await Game.filter(chat=chat[0]).order_by("-id").first()
    if not game or (game.state == GameState.ended):
        new_game = await Game.create(chat=chat[0], state=GameState.set_in_game)
        me = (await message.api.get_me()).unwrap()

        keyboard = InlineKeyboard().add(
            InlineButton(
                "join placeholder", url=f"https://t.me/{me.username}?start=join_{new_game.id}"
            )
        )
        await message.answer("set a game placeholder", reply_markup=keyboard.get_markup())


@dp.message(Markup("/start join_<game_id>"))
async def join_in_game(message: Message, game_id: int):
    game = await Game.get(id=game_id).prefetch_related("chat")
    await Player.get_or_create(uid=message.from_user.id, game=game)
    await message.reply(f"join game placeholder {game.chat.id}")
