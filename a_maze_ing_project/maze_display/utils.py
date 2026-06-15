
from enum import Enum

"""Utility file with accessible Classes, Enums and functions to
centralize the printing of colored or stylized text within a project.
Walls and Angles classes are not made to be instantiated and rather
passed as arguments for example when multiple visual themes are
made accessible to the user, so they share all the same attributes.
The styling function makes the connection between all StyleEnums,
its return value thought out to be stored or directly printed with
the style_print function. It makes from the passed Styling and
Colors Enum values a custom 'theme' that can group as as many effects
as one could want. For colors, the values can range from 0 to 255 and
be inserted as value from the Colors enum, a string or an int of the
values. No verification of range is made, feel free to experiment
until the output style is to your liking.
"""

class Keyboard(Enum):
    """Stores in lists of strings the different keyboard keys available to
    navigate menues. Contains characters or escape sequences for
    ESCAPE, CONFIRM, UP, DOWN, RIGHT and LEFT.
    """
    ESCAPE = "\x1b"
    CONFIRM = ("\r", "\n")
    UP = ("w", "A", "\x1b[A", "\x1b", "\xe0H")
    DOWN = ("s", "B", "\x1b[B", "\x1b", "\xe0P")
    RIGHT = ("d", "C", "\x1b[C", "\x1b", "\xe0M")
    LEFT = ("a", "D", "\x1b[D", "\x1b", "\xe0K")


class Walls:
    """Parent class of Walls classes declaring attributes to be used in
    displays, to avoid attributes errors. Contains only attributes
    as string constants, representing different available special
    characters to make up the blocks's walls.

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
    DOT: str


class BasicWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS, DOT
    """
    VERTICAL: str = "│"
    HORIZONTAL: str = "─"

    VERTICAL_R: str = "├"
    VERTICAL_L: str = "┤"
    HORIZONTAL_U: str = "┴"
    HORIZONTAL_D: str = "┬"
    CROSS: str = "┼"
    DOT: str = "·"


class BoldBasicWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS, DOT
    """
    VERTICAL: str = "┃"
    HORIZONTAL: str = "━"

    VERTICAL_R: str = "┣"
    VERTICAL_L: str = "┫"
    HORIZONTAL_U: str = "┻"
    HORIZONTAL_D: str = "┳"
    CROSS: str = "╋"
    DOT: str = "•"


class DoubleWalls(Walls):
    """Class child of Walls, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: VERTICAL, HORIZONTAL, VERTICAL_R, VERTICAL_L,
    HORIZONTAL_U, HORIZONTAL_D, CROSS, DOT
    """
    VERTICAL: str = "║"
    HORIZONTAL: str = "═"

    VERTICAL_R: str = "╠"
    VERTICAL_L: str = "╣"
    HORIZONTAL_U: str = "╩"
    HORIZONTAL_D: str = "╦"
    CROSS: str = "╬"
    DOT: str = "◦"


class Angles:
    """Parent class of Angles classes declaring attributes to be used in
    displays, to avoid attributes errors. Contains only attributes
    as string constants, representing different available special
    characters to make up the blocks's angles.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str
    TOP_RIGHT: str
    BOTTOM_LEFT: str
    BOTTOM_RIGHT: str


class BasicAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "┌"
    TOP_RIGHT: str = "┐"
    BOTTOM_LEFT: str = "└"
    BOTTOM_RIGHT: str = "┘"


class BoldBasicAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "┏"
    TOP_RIGHT: str = "┓"
    BOTTOM_LEFT: str = "┗"
    BOTTOM_RIGHT: str = "┛"


class DoubleAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "╔"
    TOP_RIGHT: str = "╗"
    BOTTOM_LEFT: str = "╚"
    BOTTOM_RIGHT: str = "╝"


class RoundedAngles(Angles):
    """Class child of Angles, assigning values to its declared attributes,
    to be used in blocks and menues displays.

    Attributes: TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT
    """
    TOP_LEFT: str = "╭"
    TOP_RIGHT: str = "╮"
    BOTTOM_LEFT: str = "╰"
    BOTTOM_RIGHT: str = "╯"


class StyleEnum(Enum):
    """Enum containing a single __str__ method to be inherited by other
    Enums. Useful to directly return the attributes values when the
    StyleEnums are called in prints functions, rather than their
    name.
    """
    def __str__(self) -> str:
        return str(self.value)


class Shades(StyleEnum):
    """StyleEnum containing different shade characters for all purposes.
    """
    BLOCK = "█"
    DARK_SHADE = "▓"
    MEDIUM_SHADE = "▒"
    LIGHT_SHADE = "░"


class SmallIcons(StyleEnum):
    """StyleEnum containing single character icons to be used directly in
    prints.

    Note: emoji characters are two spaces wide. The below-declared emoji_list
    exposes them, and can be used in a condition to print an extra space
    if a non-emoji character is used in the same place.
    """
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


emoji_list: list[SmallIcons] = [
    SmallIcons.COOKIE,
    SmallIcons.BEE,
    SmallIcons.FLOWER,
    SmallIcons.TONGUE,
    SmallIcons.BIKINI,
    SmallIcons.CATERPILLAR,
    SmallIcons.COW,
    SmallIcons.MILK,
    SmallIcons.BUTTERFLY
]


class Colors(StyleEnum):
    """StyleEnum containing string constants representing color codes to
    be used in ASCII escape sequences during style printing.
    """
    DEFAULT = "-1"
    BLACK = "0"
    GRAY = "250"
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

    Some of these codes won't work depending on the terminal, and testing only
    will be able to make sure the terminal your program will support will work
    with the wanted effects.
    """
    BOLD = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINED = "4"
    DOUBLE_UNDERLINE = "21"
    BLINKING = "5"
    INVERSE = "7"
    INVISIBLE = "8"
    STRIKETHROUGH = "9"


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

    Some of these codes won't work depending on the terminal, and testing only
    will be able to make sure the terminal your program will support will work
    with the wanted effects.
    """
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
        fg_color: Colors | str | int = Colors.DEFAULT,
        bg_color: Colors | str | int = Colors.DEFAULT) -> str:
    """Returns a string to print to apply a custom style. Takes as argument
    a list of Styling values [BOLD, ITALIC, ...], a foreground color
    and a background color.

    Note: style is not applied to MOVE values of CursorOperations.
    """
    return (f"\033[0;{";".join([
        *(str(st) for st in style),
        (f"38:5:{str(fg_color)}"
         if str(fg_color) is not str(Colors.DEFAULT) else "39"),
        (f"48:5:{str(bg_color)}"
         if str(bg_color) is not str(Colors.DEFAULT) else "49")
        ])}m")


def style_print(
        style: str, content: str, end: str = "", flush: bool = True) -> None:
    """Takes a style, a string content and an optional end string to print out
    respecting this order: print(style, content, STYLE_CLEAR, end).
    Sep and end argument to print are emptied.
    """
    print(
        style, content, CursorOperations.STYLE_CLEAR, end,
        flush=flush, sep="", end="")


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
