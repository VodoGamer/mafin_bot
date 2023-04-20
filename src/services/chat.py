from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chat:
    chat_id: int
    title: str
