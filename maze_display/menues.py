
from .utils import style_print, SmallIcons
from .display import print_error
from .themes import Theme
from random import randint
from typing import cast
from enum import Enum
from collections.abc import Callable
from functools import partial
from itertools import chain


class ProgramQuit(Exception):
    pass


class Keyboard(Enum):
    ESCAPE = "\x1b"
    UP = "\x1b[A"
    DOWN = "\x1b[B"
    RIGHT = "\x1b[C"
    LEFT = "\x1b[D"


def instantiate_menues(
        config: dict[str, str]) -> Callable[[str, str | Theme], str | None]:

    config_save: dict[str, str] = config.copy()
    current_menu: str = "main"
    current_index: int = 0
    current_error: str = ""
    focused_option: Option | None = None

    def get_config_ranges(option: str) -> range | tuple[range, range]:
        match option:
            case "height" | "width" | "seed":
                return range(0, 1000000000000)
            case "entry" | "exit":
                return (
                    range(0, int(config["width"])),
                    range(0, int(config["height"])))
            case _:
                return range(0)

    def change_menu(new_menu: str) -> None:
        nonlocal current_menu
        nonlocal current_index
        nonlocal current_error
        if (current_menu == "maze_config"
                and current_index == len(menues["maze_config"]) - 1):
            config.update(config_save)
        current_menu = new_menu
        current_index = 0
        current_error = ""
        if current_menu == "maze_config":
            config_save.update(config)
        return ""

    def leave_program(_: str) -> None:
        print("Hihi !")
        raise ProgramQuit

    def randomize_seed() -> None:
        config["seed"] = randint(0, 1000000000000)

    def generate_new_maze() -> str:
        return "maze_gen"

    class Option:
        def __init__(
                self, name: str, option_type: str,
                text: str, options: list[str] | None = None,
                exec: Callable[[str], None] | None = None) -> None:
            self.name: str = name
            self.option_type: str = option_type
            self.current_option: int = 0
            self.options: list[str] = options
            self.text: str = text
            self.exec: Callable[[str], None] | None = exec

        def __str__(self) -> str:
            if config.get(self.name) is not None:
                return self.text.format(value=config.get(self.name))
            return self.text

        def toggle(self):
            if config[self.name] == "True":
                config[self.name] = "False"
            else:
                config[self.name] = "True"

        def value_up(self, factor: int) -> None:
            if self.option_type == "slider":
                value: int = int(config[self.name])
                value += factor
                value_range: range = get_config_ranges(self.name)
                if value > value_range[-1]:
                    value = value_range[0]
                config[self.name] = str(value)
            elif self.option_type == "double_slider":
                values: list[int, int] = [
                    int(config[self.name].split(",")[0]),
                    int(config[self.name].split(",")[1])]
                values[self.current_option] += factor
                value_range: range = get_config_ranges(
                    self.name)[self.current_option]
                if values[self.current_option] > value_range[-1]:
                    values[self.current_option] = value_range[0]
                config[self.name] = ",".join([str(value) for value in values])

        def value_down(self, factor: int) -> None:
            if self.option_type == "slider":
                value: int = int(config[self.name])
                value -= factor
                value_range: range = get_config_ranges(self.name)
                if value < value_range[0]:
                    value = value_range[-1]
                config[self.name] = str(value)
            elif self.option_type == "double_slider":
                values: list[int, int] = [
                    int(config[self.name].split(",")[0]),
                    int(config[self.name].split(",")[1])]
                values[self.current_option] -= factor
                value_range: range = get_config_ranges(
                    self.name)[self.current_option]
                if values[self.current_option] < value_range[0]:
                    values[self.current_option] = value_range[-1]
                config[self.name] = ",".join([str(value) for value in values])

        def value_left(self) -> None:
            if self.option_type in ("slider, double_slider"):
                self.value_down(10)
            elif self.option_type == "selection":
                config[self.name] = self.options[
                    self.options.index(config[self.name]) - 1]

        def value_right(self) -> None:
            if self.option_type in ("slider, double_slider"):
                self.value_up(10)
            elif self.option_type == "selection":
                config[self.name] = self.options[
                    (self.options.index(config[self.name]) + 1)
                    % len(self.options)]

        def browse_option(self, user_input: str) -> None:
            if user_input in ("s", Keyboard.DOWN.value):
                self.value_down(1)
            elif user_input in ("w", Keyboard.UP.value):
                self.value_up(1)
            elif user_input in ("a", Keyboard.LEFT.value):
                self.value_left()
            elif user_input in ("w", Keyboard.RIGHT.value):
                self.value_right()
            elif user_input == "\r":
                if (
                        self.option_type == "double_slider"
                        and self.current_option == 0):
                    self.current_option = 1
                else:
                    self.current_option = 0
                    nonlocal focused_option
                    focused_option = None

    menues: dict[str, list[Option]]
    menues = {
        "main": [
            Option(
                name="show path",
                option_type="toggle",
                text="Show/Hide found path"),
            Option(
                name="theme",
                option_type="validate",
                text="Change current theme",
                exec=partial(change_menu, "theme")),
            Option(
                name="save maze",
                option_type="validate",
                text="Save maze to output file"),
            Option(
                name="generate",
                option_type="validate",
                text="Generate new maze",
                exec=partial(change_menu, "maze_config")),
            Option(
                name="quit",
                option_type="validate",
                text="Quit A_maze_ing",
                exec=partial(leave_program, ""))],
        "maze_config": [
            Option(
                name="width",
                option_type="slider",
                text=f"{"Width:":<22}""{value:>13}"),
            Option(
                name="height",
                option_type="slider",
                text=f"{"Height:":<22}""{value:>13}"),
            Option(
                name="entry",
                option_type="double_slider",
                text=f"{"Entry:":<22}""{value:>13}"),
            Option(
                name="exit",
                option_type="double_slider",
                text=f"{"Exit:":<22}""{value:>13}"),
            Option(
                name="perfect",
                option_type="toggle",
                text=f"{"Perfect:":<22}""{value:>13}"),
            Option(
                name="central_icon",
                option_type="toggle",
                text=f"{"Central icon:":<22}""{value:>13}"),
            Option(
                name="gen_algorithm",
                option_type="selection",
                options=["Backtracking", "Prim"],
                text=(
                    f"{"Generation algorithm:":<22}"
                    "{value:>13}")),
            Option(
                name="sol_algorithm",
                option_type="selection",
                options=["Dijkstra"],
                text=(
                    f"{"Solving algorithm:":<22}"
                    "{value:>13}")),
            Option(
                name="seed",
                option_type="slider",
                text=f"{"Generation seed:":<22}""{value:>13}"),
            Option(
                name="randomize seed",
                option_type="validate",
                text="Randomize seed",
                exec=randomize_seed),
            Option(
                name="output_file",
                option_type="text",
                text=f"{'Output file:':<22}""{value:>13}"),
            Option(
                name="generate maze",
                option_type="validate",
                text="- Generate maze -",
                exec= generate_new_maze),
            Option(
                name="back",
                option_type="validate",
                text="return",
                exec=partial(change_menu, "main"))]}

    def browse_menu(user_input: str) -> str:
        nonlocal current_index
        nonlocal current_menu
        nonlocal focused_option
        if user_input == Keyboard.ESCAPE.value:
            if focused_option is not None:
                focused_option = None
            elif current_menu != "main":
                current_menu = "main"
        elif focused_option is not None:
            focused_option.browse_option(user_input)
        elif user_input in ("s", Keyboard.DOWN.value):
            current_index += 1
            if current_index > len(menues[current_menu]) - 1:
                current_index = 0
        elif user_input in ("w", Keyboard.UP.value):
            current_index -= 1
            if current_index < 0:
                current_index =  len(menues[current_menu]) - 1
        elif user_input == "\r":
            if menues[current_menu][current_index].option_type == "validate":
                return menues[current_menu][current_index].exec()
            elif menues[current_menu][current_index].option_type == "toggle":
                menues[current_menu][current_index].toggle()
            else:
                focused_option = menues[current_menu][current_index]

    def print_menu(theme: Theme) -> None:
        nonlocal current_menu
        nonlocal current_index
        nonlocal current_error
        nonlocal focused_option
        menu_width: int = max(
            len(str(entry)) for entry in chain(
                menues[current_menu], current_error.split("\n"))) + 6
        line: str = (
            theme.angles.TOP_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.TOP_RIGHT)
        style_print(theme.walls_style, line.center(
            int(config_save["width"]) * 4), "\n")
        for index, entry in enumerate(menues[current_menu]):
            if index == len(menues[current_menu]) - 1 and current_error == "":
                style_print(theme.walls_style, (
                    f"{theme.walls.VERTICAL}{" " * menu_width}"
                    f"{theme.walls.VERTICAL}").center(
                        int(config_save["width"]) * 4),
                    "\n")
            elif index == len(menues[current_menu]) - 1:
                for errors in current_error.split("\n"):
                    style_print(
                        theme.walls_style, theme.walls.VERTICAL.rjust(int(
                            (int(config_save["width"]) * 4 - menu_width) / 2)))
                    print_error(errors.center(menu_width),  end="")
                    style_print(theme.walls_style, theme.walls.VERTICAL, "\n")
            if index == current_index:
                line = (
                    ("\033[4m" if focused_option == entry else "") + (
                    f"{SmallIcons.LEFT_ARROW} {entry} "
                    f"{SmallIcons.RIGHT_ARROW}").center(menu_width))
            else:
                line = (str(entry).center(menu_width))
            style_print(
                theme.walls_style, theme.walls.VERTICAL.rjust(
                    int((int(config_save["width"]) * 4 - menu_width) / 2)))
            style_print(
                theme.icon_style, line.center(menu_width))
            style_print(theme.walls_style, theme.walls.VERTICAL, "\n")
        line: str = (
            theme.angles.BOTTOM_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.BOTTOM_RIGHT)
        style_print(theme.walls_style, line.center(
            int(config_save["width"]) * 4), "\n")

    def menues_module(
            current_action: str, user_input: str | Theme) -> str | None:
        if current_action == "browse_menu":
            return browse_menu(cast(str, user_input))
        elif current_action == "print_menu":
            print_menu(cast(Theme, user_input))
        elif current_action == "maze_gen_error":
            nonlocal current_error
            current_error = user_input

    return menues_module
