
from enum import Enum


class StyleEnum(Enum):
    def __str__(self) -> str:
        return str(self.value)


class Walls:
    VERTICAL: str
    HORIZONTAL: str

    VERTICAL_R: str
    VERTICAL_L: str
    HORIZONTAL_U: str
    HORIZONTAL_D: str
    CROSS: str


class BasicWalls(Walls):
    VERTICAL: str = "│"
    HORIZONTAL: str = "─"

    VERTICAL_R: str = "├"
    VERTICAL_L: str = "┤"
    HORIZONTAL_U: str = "┴"
    HORIZONTAL_D: str = "┬"
    CROSS: str = "┼"


class BoldBasicWalls(Walls):
    VERTICAL: str = "┃"
    HORIZONTAL: str = "━"

    VERTICAL_R: str = "┣"
    VERTICAL_L: str = "┫"
    HORIZONTAL_U: str = "┻"
    HORIZONTAL_D: str = "┳"
    CROSS: str = "╋"


class DoubleWalls(Walls):
    VERTICAL: str = "║"
    HORIZONTAL: str = "═"

    VERTICAL_R: str = "╠"
    VERTICAL_L: str = "╣"
    HORIZONTAL_U: str = "╩"
    HORIZONTAL_D: str = "╦"
    CROSS: str = "╬"


class Angles:
    TOP_LEFT: str
    TOP_RIGHT: str
    BOTTOM_LEFT: str
    BOTTOM_RIGHT: str


class BasicAngles(Angles):
    TOP_LEFT: str = "┌"
    TOP_RIGHT: str = "┐"
    BOTTOM_LEFT: str = "└"
    BOTTOM_RIGHT: str = "┘"


class BoldBasicAngles(Angles):
    TOP_LEFT: str = "┏"
    TOP_RIGHT: str = "┓"
    BOTTOM_LEFT: str = "┗"
    BOTTOM_RIGHT: str = "┛"


class DoubleAngles(Angles):
    TOP_LEFT: str = "╔"
    TOP_RIGHT: str = "╗"
    BOTTOM_LEFT: str = "╚"
    BOTTOM_RIGHT: str = "╝"


class RoundedAngles(Angles):
    TOP_LEFT: str = "╭"
    TOP_RIGHT: str = "╮"
    BOTTOM_LEFT: str = "╰"
    BOTTOM_RIGHT: str = "╯"


class SmallIcons(StyleEnum):
    DARK_SHADE = "▓"
    MEDIUM_SHADE = "▒"
    LIGHT_SHADE = "░"
    NO_SHADE = " "
    FULL_SQUARE = "■"
    EMPTY_SQUARE = "□"
    ROUNDED_SQUARE = "▢"
    SQUARECEPTION = "▣"
    HOR_LINES_SQUARE = "▤"
    DIAMONDCEPTION = "◈"
    OUTLINED_X = "🯀"
    HAZARD_SYMBOL = "☣"
    RADIOACTIVE_SYMBOL = "☢"
    PLUG_FACE = "⚉"
    COOKIE = "🍪"
    BEE = "🐝"
    FLOWER = "🌸"
    CATERPILLAR = "🐛"
    BUTTERFLY = "🦋"
    PHONE = "☎"
    CUTTING_SCISSORS = "✁"
    PLANE = "✈"
    WRITING_PEN = "✎"
    CHECK_MARK = "✔"
    CIRCLED_STAR = "✪"
    LEFT_ARROW = "⏴"
    RIGHT_ARROW = "⏵"


class Colors(StyleEnum):
    BLACK = "0"
    RED = "1"
    GREEN = "2"
    YELLOW = "3"
    BLUE = "4"
    MAGENTA = "5"
    CYAN = "6"
    WHITE = "7"
    DEFAULT = "9"


class Styling(StyleEnum):
    BOLD = "1"
    DIM = "2"
    FOREGROUND = "3"
    BACKGROUND = "4"
    BLINKING = "5"


class CursorOperations(StyleEnum):
    ESC = "\033["

    SHOW_CURSOR = "\033[25h"
    HIDE_CURSOR = "\033[25l"
    SAVE_POSITION = "\033[s"
    LOAD_POSITION = "\033[u"

    LINE_CLEAR = "\033[2K"
    LIGHT_LINE_CLEAR = "\033[0K"
    LIGHT_CLEAR = "\033[0J"
    HEAVY_CLEAR = "\033[3J\033[1;0H\033[0J"
    STYLE_CLEAR = "\033[0m"


def styling(
        style: list[Styling] = [],
        fg_color: Colors = Colors.DEFAULT,
        bg_color: Colors = Colors.DEFAULT) -> str:
    return (f"\033[0;{";".join([
        *(str(st) for st in style), f"3{fg_color}", f"4{bg_color}"])}m")


def bold_style(color: Colors = Colors.DEFAULT) -> str:
    return f"\033[3{color};1m"


def move_cursor(y: int, x: int = 0) -> str:
    coordinate = "\033[" + str(y) + ";" + str(x) + "H"
    return coordinate


def style_print(style: Styling | str, content: str, end: str = "") -> None:
    print(
        style, content, end, CursorOperations.STYLE_CLEAR,
        flush=True, sep="", end="")
