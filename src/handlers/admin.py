from telegrinder import Dispatch, Message
from telegrinder.rules import Text

# from src.bot.init import api
# from src.handlers.enrollment import update_enrollment_message
from src.rules import IsAdmin

dp = Dispatch()
# TODO: admin commands


@dp.message(IsAdmin(), Text("/delete_chat"))
async def delete_chat(message: Message):
    # chat = await Chat.get(id=message.chat.id)
    # await chat.delete()
    # await message.reply(f"{chat.id=} deleted")
    return


@dp.message(IsAdmin(), Text("/delete_game"))
async def delete_chat_game(message: Message):
    # game = await Game.get(chat_id=message.chat.id).prefetch_related("messages", "chat")
    # for game_message in game.messages:
    #     await api.delete_message(chat_id=game.chat.id, message_id=game_message.message_id)
    # await game.delete()
    # await message.reply(f"{game.id=} deleted")
    return


@dp.message(IsAdmin(), Text("/kick_me"))
async def kick_admin_from_games(message: Message):
    # player = await Player.get(id=message.from_user.id)
    # game = await Game.get(players__id=player.id).prefetch_related("chat")
    # enrollment_message = await GameMessage.get(game=game, payload=MessagePayload.enrollment)
    # players = await Player.filter(game=game).exclude(id=player.id)
    # await player.delete()
    # await update_enrollment_message(
    # game.chat.id, game.id, enrollment_message.message_id, players)
    # await message.reply(f"{player.id=} kicked")
    return
