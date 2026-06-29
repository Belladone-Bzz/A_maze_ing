
from enum import Enum
from typing import cast
from .utils import Styling, styling, Colors, Walls, Angles, Shades
from .utils import (
    BasicWalls, BoldBasicWalls, DoubleWalls,
    BoldBasicAngles, DoubleAngles, RoundedAngles,
    SmallIcons)


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
    MEUUH = (
        (0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0),
        (1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0),
        (0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        (1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0),
        (0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0),
        (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1),
        (0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1),
        (0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0),
        (0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0),
        (0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0))


class Theme:
    """Class destined to group together special characters and style printing
    for the Maze's walls, angles, the start and exit characters, the
    path visuals and the pattern's. Consists of an init method only. Uses
    Walls, Angles, SmallIcons classes, and styling function.

    Attributes: Walls, Angles, start, exit, path_chars(Walls, Angles)
    walls_ path_ start_ exit_ icon_ styles as str, icon_ Walls, Angles and
    content.
    """
    def __init__(
            self, walls: type[Walls], angles: type[Angles],
            start: SmallIcons, exit: SmallIcons,
            path_chars: tuple[type[Walls], type[Angles]],
            walls_style: str, path_style: str,
            start_style: str, exit_style: str,
            visited_style: str, highlighted_style: str,
            icon_walls: type[Walls], icon_angles: type[Angles],
            icon_content: str, icon_style: str):
        self.walls: type[Walls] = walls
        self.angles: type[Angles] = angles
        self.start: SmallIcons = start
        self.exit: SmallIcons = exit
        self.path_chars: tuple[type[Walls], type[Angles]] = path_chars
        self.walls_style: str = walls_style
        self.path_style: str = path_style
        self.start_style: str = start_style
        self.exit_style: str = exit_style
        self.visited_style: str = visited_style
        self.highlighted_style: str = highlighted_style
        self.icon_walls: type[Walls] = icon_walls
        self.icon_angles: type[Angles] = icon_angles
        self.icon_content: str = icon_content
        self.icon_style: str = icon_style


class Themes(Enum):
    """Enumerates different Theme objects with set values for each argument.
    Used in parser, menues and maze displays.
    """
    DEFAULT = Theme(
        walls=BoldBasicWalls,
        angles=BoldBasicAngles,
        start=SmallIcons.EMPTY_SQUARE,
        exit=SmallIcons.FULL_SQUARE,
        path_chars=(BasicWalls, RoundedAngles),

        walls_style=styling(),
        path_style=styling([Styling.BOLD], Colors.RED),
        start_style=styling([Styling.BOLD], Colors.RED),
        exit_style=styling([Styling.BOLD], Colors.RED),
        visited_style=styling([], Colors.GRAY),
        highlighted_style=styling([], Colors.WHITE),

        icon_walls=DoubleWalls,
        icon_angles=DoubleAngles,
        icon_content="   ",

        icon_style=styling([Styling.BOLD], Colors.YELLOW))
    BEES = Theme(
        walls=BasicWalls,
        angles=RoundedAngles,
        start=SmallIcons.BEE,
        exit=SmallIcons.FLOWER,
        path_chars=(BasicWalls, RoundedAngles),

        walls_style=styling([], Colors.BLACK, Colors.YELLOW),
        path_style=styling([], "208", Colors.YELLOW),
        start_style=styling([], Colors.BLACK, Colors.YELLOW),
        exit_style=styling([], Colors.BLACK, Colors.YELLOW),
        visited_style=styling([], Colors.GRAY, Colors.YELLOW),
        highlighted_style=styling([], "12", Colors.YELLOW),

        icon_walls=DoubleWalls,
        icon_angles=DoubleAngles,
        icon_content=str(Shades.BLOCK) * 3,

        icon_style=styling([], Colors.BLACK, Colors.YELLOW))
    METAMORPHOSIS = Theme(
        walls=BasicWalls,
        angles=RoundedAngles,
        start=SmallIcons.CATERPILLAR,
        exit=SmallIcons.BUTTERFLY,
        path_chars=(BasicWalls, RoundedAngles),

        walls_style=styling([], Colors.LIGHT_GREEN, Colors.MAGENTA),
        path_style=styling([], "154", Colors.MAGENTA),
        start_style=styling([], Colors.LIGHT_GREEN, Colors.MAGENTA),
        exit_style=styling([], Colors.LIGHT_GREEN, Colors.MAGENTA),
        visited_style=styling([], Colors.BLACK, Colors.MAGENTA),
        highlighted_style=styling(),

        icon_walls=DoubleWalls,
        icon_angles=DoubleAngles,
        icon_content="   ",

        icon_style=styling([Styling.BOLD], Colors.MAGENTA))
    MEUUH = Theme(
        walls=DoubleWalls,
        angles=DoubleAngles,
        start=SmallIcons.COW,
        exit=SmallIcons.MILK,
        path_chars=(DoubleWalls, DoubleAngles),

        walls_style=styling([], Colors.GREEN),
        path_style=styling([], Colors.WHITE),
        start_style=styling([], Colors.GREEN),
        exit_style=styling([], Colors.GREEN),
        visited_style=styling([], Colors.GRAY),
        highlighted_style=styling(),

        icon_walls=BoldBasicWalls,
        icon_angles=BoldBasicAngles,
        icon_content="▞▞▞",

        icon_style=styling([], Colors.WHITE))
    BOSS_LADY = Theme(
        walls=DoubleWalls,
        angles=DoubleAngles,
        start=SmallIcons.TONGUE,
        exit=SmallIcons.BIKINI,
        path_chars=(BasicWalls, RoundedAngles),

        walls_style=styling([], Colors.MAGENTA, Colors.BLACK),
        path_style=styling([], Colors.RED, Colors.BLACK),
        start_style=styling(bg_color=Colors.BLACK),
        exit_style=styling(bg_color=Colors.BLACK),
        visited_style=styling([], "253", Colors.BLACK),
        highlighted_style=styling([], "200", Colors.BLACK),

        icon_walls=BoldBasicWalls,
        icon_angles=BoldBasicAngles,
        icon_content="BBL",

        icon_style=styling(
            [Styling.ITALIC, Styling.BOLD, Styling.BLINKING],
            Colors.WHITE, Colors.BLACK)
    )


def get_theme(theme: str) -> Theme:
    """Returns a selected Theme object from the Enumeration from the
    given string as argument.
    """
    return cast(Theme, getattr(Themes, theme.upper()).value)
