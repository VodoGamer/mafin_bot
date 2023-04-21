from dataclasses import dataclass

from src.bot.init import db
from src.services.abc import read_query


@dataclass(frozen=True, slots=True)
class Chat:
    chat_id: int
    title: str


async def delete_chat(chat_id: int):
    await db.query(read_query("delete_chat.edgeql"), chat_id=chat_id)
