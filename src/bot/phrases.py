from typing import NamedTuple

from telegrinder.tools import MarkdownFormatter


class Phrase(NamedTuple):
    text: str
    PARSE_MODE: str


SET_GAME_COMMAND = "/set_in_game"


# commands
start_command = Phrase(
    f"Для начала игры в {MarkdownFormatter('МАФИНЫ').bold()} введите команду "
    f"{MarkdownFormatter(SET_GAME_COMMAND).escape()}",
    MarkdownFormatter.PARSE_MODE,
)
set_game_0_players = Phrase(
    f"{MarkdownFormatter('Набор в игру').bold()}\nЧтобы присоединиться нажми на кнопку ниже",
    MarkdownFormatter.PARSE_MODE,
)
set_game_with_players = Phrase(
    MarkdownFormatter("Набор в игру").bold() + "\nПрисоединились:\n{players}\n\n"
    "{players_count} игрока\\(ов\\)😎",
    MarkdownFormatter.PARSE_MODE,
)
