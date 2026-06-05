
from enum import Enum


class StyleEnum(Enum):
    """Enum containing a single __str__ method to be inherited by other
    Enums. Useful to directly return the attributes values when the
    StyleEnums are called in prints functions, rather than their
    name.
    """
    def __str__(self) -> str:
        return str(self.value)


class Walls:
    """Parent class of Walls classes declaring attributes to be used in
    displays, to avoid attributes errors. Contains only attributes
    as string constants, representing different available special
    characters to make up the Maze's walls.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS
    """
    VERTICAL: str
    HORIZONTAL: str

    VERTICAL_R: str
    VERTICAL_L: str
    HORIZONTAL_U: str
    HORIZONTAL_D: str
    CROSS: str


class BasicWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS
    """
    VERTICAL: str = "│"
    HORIZONTAL: str = "─"

    VERTICAL_R: str = "├"
    VERTICAL_L: str = "┤"
    HORIZONTAL_U: str = "┴"
    HORIZONTAL_D: str = "┬"
    CROSS: str = "┼"


class BoldBasicWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS
    """
    VERTICAL: str = "┃"
    HORIZONTAL: str = "━"

    VERTICAL_R: str = "┣"
    VERTICAL_L: str = "┫"
    HORIZONTAL_U: str = "┻"
    HORIZONTAL_D: str = "┳"
    CROSS: str = "╋"


class DoubleWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS
    """
    VERTICAL: str = "║"
    HORIZONTAL: str = "═"

    VERTICAL_R: str = "╠"
    VERTICAL_L: str = "╣"
    HORIZONTAL_U: str = "╩"
    HORIZONTAL_D: str = "╦"
    CROSS: str = "╬"


class Angles:
    """Parent class of Angles classes declaring attributes to be used in
    displays, to avoid attributes errors. Contains only attributes
    as string constants, representing different available special
    characters to make up the Maze's angles.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str
    TOP_RIGHT: str
    BOTTOM_LEFT: str
    BOTTOM_RIGHT: str


class BasicAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "┌"
    TOP_RIGHT: str = "┐"
    BOTTOM_LEFT: str = "└"
    BOTTOM_RIGHT: str = "┘"


class BoldBasicAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "┏"
    TOP_RIGHT: str = "┓"
    BOTTOM_LEFT: str = "┗"
    BOTTOM_RIGHT: str = "┛"


class DoubleAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "╔"
    TOP_RIGHT: str = "╗"
    BOTTOM_LEFT: str = "╚"
    BOTTOM_RIGHT: str = "╝"


class RoundedAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in Maze and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "╭"
    TOP_RIGHT: str = "╮"
    BOTTOM_LEFT: str = "╰"
    BOTTOM_RIGHT: str = "╯"


class SmallIcons(StyleEnum):
    """StyleEnum containing single character icons to be used as Maze's
    start and exit, or Pattern's content.
    """
    BLOCK = "█"
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
    TONGUE = "👅"
    BIKINI = "👙"
    CATERPILLAR = "🐛"
    COW = "🐄"
    MILK = "🥛"
    BUTTERFLY = "🦋"
    PHONE = "☎"
    CUTTING_SCISSORS = "✁"
    PLANE = "✈"
    WRITING_PEN = "✎"
    CHECK_MARK = "✔"
    CIRCLED_STAR = "✪"
    LEFT_ARROW = "⏴"
    RIGHT_ARROW = "⏵"


class Patterns(Enum):
    """Enum containing Patterns as tuples of tuples of binary values that
    will be used a booleans to update the Maze's cells as part of the
    Pattern. Makes drawings in the Maze's center that will be displayed
    with a custom theming.
    """
    NONE = ()
    FORTY_TWO = (
        (0, 0, 1, 0, 1, 1, 1),
        (0, 1, 0, 0, 0, 0, 1),
        (1, 1, 1, 0, 0, 1, 0),
        (0, 0, 1, 0, 1, 0, 0),
        (0, 0, 1, 0, 1, 1, 1))
    HEART = (
        (0, 1, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (0, 1, 0, 1, 0),
        (0, 0, 1, 0, 0))
    BEE = (
        (0, 0, 1, 1, 0, 1, 1, 0, 0, 0),
        (0, 1, 0, 0, 1, 0, 0, 1, 0, 0),
        (0, 0, 1, 0, 0, 1, 0, 1, 0, 0),
        (0, 0, 0, 1, 1, 1, 1, 1, 0, 0),
        (0, 0, 1, 1, 0, 1, 0, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 0, 0, 1),
        (1, 1, 0, 1, 0, 1, 0, 1, 0, 1),
        (0, 1, 0, 1, 0, 1, 0, 0, 0, 1),
        (0, 0, 1, 1, 0, 1, 0, 0, 1, 0),
        (0, 0, 0, 1, 1, 1, 1, 1, 0, 0))
    BBL = (
        (1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0),
        (1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0),
        (1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1))
    SIX_SEVEN = (
        (0, 1, 0, 0, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 0, 0, 1, 0),
        (1, 0, 1, 0, 0, 1, 0),
        (0, 1, 1, 0, 0, 1, 0))


class Colors(StyleEnum):
    """StyleEnum containing string constants representing color codes to
    be used in ASCII escape sequences during style printing.
    """
    DEFAULT = "-1"
    BLACK = "16"
    RED = "196"
    LIGHT_GREEN = "153"
    GREEN = "28"
    YELLOW = "220"
    BLUE = "27"
    MAGENTA = "141"
    CYAN = "81"
    WHITE = "231"


class Styling(StyleEnum):
    """StyleEnum containing string constants representing style codes to
    be used in ASCII escape sequences during style printing.
    """
    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINED = "4"
    BLINKING = "5"


def move_cursor(y: int, x: int = 0) -> str:
    """Returns a string to print to move the cursor across the terminal window
    based on the given coordinates as argument.
    """
    coordinate = "\033[" + str(y) + ";" + str(x) + "H"
    return coordinate


class CursorOperations(StyleEnum):
    """StyleEnum containing string constants representing cursor operations
    codes to be used in ASCII escape sequences during style printing.

    Examples: SAVE_CURSOR to save its position, LOAD_CURSOR to load it back
    etc.
    """
    ESC = "\033["

    SHOW_CURSOR = "\033[25h"
    HIDE_CURSOR = "\033[25l"
    SAVE_CURSOR = "\033[s"
    LOAD_CURSOR = "\033[u"
    MOVE_CURSOR = move_cursor

    MOVE_UP = "\033[A"
    MOVE_DOWN = "\033[B"
    MOVE_RIGHT = "\033[C"
    MOVE_LEFT = "\033[D"

    LINE_CLEAR = "\033[2K"
    LIGHT_LINE_CLEAR = "\033[0K"
    LIGHT_CLEAR = "\033[0J"
    HEAVY_CLEAR = "\033[3J\033[1;0H\033[0J"
    STYLE_CLEAR = "\033[0m"


def styling(
        style: list[Styling] = [],
        fg_color: Colors = Colors.DEFAULT,
        bg_color: Colors = Colors.DEFAULT) -> str:
    """Returns a string to print to apply a custom style. Takes as argument
    a list of Styling values [BOLD, ITALIC, ...], a foreground color
    and a background color.

    Note: style is not applied to MOVE values of CursorOperations.
    """
    return (f"\033[0;{";".join([
        *(str(st) for st in style),
        (f"38:5:{fg_color}" if fg_color is not Colors.DEFAULT else "39"),
        (f"48:5:{bg_color}" if bg_color is not Colors.DEFAULT else "49")])}m")


def print_error(
        content: str,
        end: str = "\n\nRefer to the provided README file for guidance.\n\n"
        ) -> None:
    """Prints messages using a bold red style destined to errors. Takes a
    message as argument, as well as an end message, defaulted to README
    redirections.

    Returns None
    """
    style_print(styling([Styling.BOLD], Colors.RED), content, end)


def style_print(style: Styling | str, content: str, end: str = "") -> None:
    """Takes a style, a string content and an optional end string to print out
    respecting this order: print(style, content, STYLE_CLEAR, end).
    Sep and end argument to print are emptied.
    """
    print(
        style, content, CursorOperations.STYLE_CLEAR, end,
        flush=True, sep="", end="")
