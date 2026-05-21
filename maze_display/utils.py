
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


class DoubleWalls(Walls):
    VERTICAL: str = "║"
    HORIZONTAL: str = "═"

    HORIZONTAL_R: str = "╠"
    HORIZONTAL_L: str = "╣"
    VERTICAL_U: str = "╩"
    VERTICAL_D: str = "╦"
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
    PHONE = "☎"
    CUTTING_SCISSORS = "✁"
    PLANE = "✈"
    WRITING_PEN = "✎"
    CHECK_MARK = "✔"
    CIRCLED_STAR = "✪"


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

    BOLD = "1"
    DIM = "2"
    FOREGROUND = "3"
    BACKGROUND = "4"
    BLINKING = "5"
    STYLE = "m"

    NO_STYLE = ""
    BOLD_YELLOW = ESC + f"{FOREGROUND}{Colors.YELLOW};{BOLD}{STYLE}"


class Theme:
    def __init__(
            self, walls: type[Walls], angles: type[Angles],
            start: SmallIcons, exit: SmallIcons,
            progress_line: tuple[type[Walls], type[Angles]],
            walls_style: Styling, path_style: Styling,
            start_style: Styling, exit_style: Styling,
            icon_walls: type[Walls], icon_angles: type[Angles],
            icon_style: Styling):
        self.walls = walls
        self.angles = angles
        self.start = start
        self.exit = exit
        self.progress_line = progress_line
        self.walls_style = walls_style
        self.path_style = path_style
        self.start_style = start_style
        self.exit_style = exit_style
        self.icon_walls = icon_walls
        self.icon_angles = icon_angles
        self.icon_style = icon_style


def get_theme(name: str) -> Theme:
    if name == "basic":
        return Theme(
            walls=BasicWalls,
            angles=BasicAngles,
            start=SmallIcons.EMPTY_SQUARE,
            exit=SmallIcons.FULL_SQUARE,
            progress_line=(BasicWalls, RoundedAngles),

            walls_style=Styling.NO_STYLE,
            path_style=Styling.BOLD_YELLOW,
            start_style=Styling.BOLD_YELLOW,
            exit_style=Styling.BOLD_YELLOW,

            icon_walls=DoubleWalls,
            icon_angles=DoubleAngles,

            icon_style=Styling.BOLD_YELLOW)
    raise ValueError


def move_cursor(y: int, x: int = 0) -> str:
    coordinate = "\033[" + str(y) + ";" + str(x) + "H"
    return coordinate


def style_print(style: Styling, content: str, end: str = "") -> None:
    print(style, content, end, Styling.STYLE_CLEAR, sep="", end="")
