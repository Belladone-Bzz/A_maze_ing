
from .utils import Styling, styling, Colors, Walls, Angles
from .utils import (
    BasicWalls, BoldBasicWalls, DoubleWalls,
    BasicAngles, BoldBasicAngles, DoubleAngles, RoundedAngles,
    SmallIcons)


class Theme:
    def __init__(
            self, walls: type[Walls], angles: type[Angles],
            start: SmallIcons, exit: SmallIcons,
            visited_background: SmallIcons,
            progress_line: tuple[type[Walls], type[Angles]],
            walls_style: str, path_style: str,
            start_style: str, exit_style: str,
            icon_walls: type[Walls], icon_angles: type[Angles],
            icon_style: str):
        self.walls = walls
        self.angles = angles
        self.start = start
        self.exit = exit
        self.visited_background = visited_background
        self.progress_line = progress_line
        self.walls_style = walls_style
        self.path_style = path_style
        self.start_style = start_style
        self.exit_style = exit_style
        self.icon_walls = icon_walls
        self.icon_angles = icon_angles
        self.icon_style = icon_style


def get_themes() -> dict[str, Theme]:
    return {
        "Default": Theme(
            walls=BoldBasicWalls,
            angles=BoldBasicAngles,
            start=SmallIcons.EMPTY_SQUARE,
            exit=SmallIcons.FULL_SQUARE,
            visited_background=SmallIcons.NO_SHADE,
            progress_line=(BasicWalls, RoundedAngles),

            walls_style=styling(),
            path_style=styling([Styling.BOLD], Colors.YELLOW),
            start_style=styling([Styling.BOLD], Colors.YELLOW),
            exit_style=styling([Styling.BOLD], Colors.YELLOW),

            icon_walls=DoubleWalls,
            icon_angles=DoubleAngles,

            icon_style=styling([Styling.BOLD], Colors.YELLOW)),
        "Bees": Theme(
            walls=BasicWalls,
            angles=RoundedAngles,
            start=SmallIcons.BEE,
            exit=SmallIcons.FLOWER,
            visited_background=SmallIcons.NO_SHADE,
            progress_line=(BasicWalls, RoundedAngles),

            walls_style=styling([], Colors.YELLOW),
            path_style=styling([], Colors.YELLOW),
            start_style=styling([], Colors.YELLOW),
            exit_style=styling([], Colors.YELLOW),

            icon_walls=DoubleWalls,
            icon_angles=DoubleAngles,

            icon_style=styling([Styling.BOLD], Colors.YELLOW)),
        "Metamorphosis" : Theme(
            walls=BasicWalls,
            angles=RoundedAngles,
            start=SmallIcons.CATERPILLAR,
            exit=SmallIcons.BUTTERFLY,
            visited_background=SmallIcons.NO_SHADE,
            progress_line=(BasicWalls, RoundedAngles),

            walls_style=styling([], Colors.MAGENTA),
            path_style=styling([], Colors.YELLOW),
            start_style=styling([], Colors.MAGENTA),
            exit_style=styling([], Colors.MAGENTA),

            icon_walls=DoubleWalls,
            icon_angles=DoubleAngles,

            icon_style=styling([Styling.BOLD], Colors.MAGENTA)),
        "Meuuh": Theme(
            walls=DoubleWalls,
            angles=DoubleAngles,
            start=SmallIcons.MILK,
            exit=SmallIcons.COW,
            visited_background=SmallIcons.NO_SHADE,
            progress_line=(DoubleWalls, DoubleAngles),

            walls_style=styling([Styling.BLINKING], Colors.YELLOW),
            path_style=styling([Styling.BLINKING], Colors.GREEN),
            start_style=styling([], Colors.YELLOW),
            exit_style=styling([], Colors.YELLOW),

            icon_walls=BoldBasicWalls,
            icon_angles=BoldBasicAngles,

            icon_style=styling([Styling.ITALIC], Colors.WHITE))}
