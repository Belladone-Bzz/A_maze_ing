
from .utils import (
    style_print, print_error, SmallIcons, CursorOperations, Keyboard)
from .themes import Theme, Themes, get_theme, Patterns
from a_maze_ing_project.maze_gen.mazegenerator import Maze
from a_maze_ing_project.maze_solve import MazeSolver
from random import randint, seed
from typing import cast
from os import get_terminal_size, terminal_size
from collections.abc import Callable
from functools import partial
from itertools import chain


class ProgramQuit(Exception):
    """Custom exception caught by the a_maze_ing program in case the quit
    option is selected.
    """
    pass


def instantiate_menues(
        config: dict[str, str]) -> Callable[[str, str], str]:
    """Exposed function of the menues file, enclosing all menues-displaying
    and browsing functions. Takes a config dict to keep access to updated
    Maze infos.

    Returns a menu_module function, which takes as arguments an
    action to execute as a string, and a user_input to give out to
    pertinent functions.

    This function's enclosure contains the Option class to manage
    menues actions contained in dicts for each menu
    ("main", "maze_config"), and nonlocal current_menu, index, error and
    option to keep track of the user's actions.

    Can:
    "browse_menu": takes the user_input as argument and moves up and down
    in menues depending on navigation keys from the Keyboard Enum,
    or adjust config values with Option methods. Can return a string.
    "print_menu": based on the current_menu nonlocal string, displays the
    viewed menu with arrows to indicate the selected option, underline
    to indicate which option is being modified and potential error
    messages.
    "maze_error": Update the current error messages with the input.
    "back_to_main": change the menu back to main but overrides the config_save
    dict with that of config, to use when the Maze generation is successful.
    """

    config_save: dict[str, str] = config.copy()
    current_menu: str = "main"
    current_index: int = 0
    current_error: str = ""
    focused_option: "Option" | None = None

    def get_config_ranges(option: str) -> range | tuple[range, range]:
        """Returns set values as range of tuple of ranges for each
        available config parameter to handle minimum and maximum
        values to cycle through them from the maze config menu.
        """
        match option:
            case "height" | "width" | "seed":
                return range(0, 1000000000000)
            case "entry" | "exit":
                return (
                    range(0, int(config["width"])),
                    range(0, int(config["height"])))
            case "gen_speed":
                return range(0, 11)
            case _:
                return range(0)

    def change_menu(new_menu: str) -> str:
        """Execution function used to navigate to a new menu, updating
        the current_menu nonlocal string with the menu given as
        argument. If the user enters or leaves the maze_config menu,
        a config_save is used to update or updated with the shared
        config dict.

        Returns an empty string to respect Callable typing.
        """
        nonlocal current_menu
        nonlocal current_index
        nonlocal current_error
        if current_menu == "maze_config":
            for key, value in config_save.items():
                config[key] = value
        current_menu = new_menu
        current_index = 0
        current_error = ""
        if current_menu == "maze_config":
            for key, value in config.items():
                config_save[key] = value
        return ""

    def leave_program(_: str) -> str:
        """Execution function called to raise ProgramQuit Exception.
        Takes a string and returns one to respect Callable typing, but
        does nothing of them.
        """
        raise ProgramQuit

    def randomize_seed(_: str) -> str:
        """Execution function called to randomize the Maze config's seed.
        Takes a string and returns one to respect Callable typing, but
        does nothing of them.
        """
        temp: int = int(config["seed"])
        seed()
        config["seed"] = str(randint(0, 1000000000000))
        seed(temp)
        return ""

    class Option:
        """Option class: takes various string, list of strings and sometimes
        an execution function to handle different type of menu options.

        Attributes: takes a mandatory name, option_type and text
        argument to init, while options and exec are only necessary
        to "selection" and "validation" respectively.

        Methods: value_up, value_down, value_left, value_right, toggle,
        browse_options.
        """
        def __init__(
                self, name: str, option_type: str, text: str,
                options: list[str] = [],
                exec: partial[str] = partial(lambda _: "", "")) -> None:
            self.name: str = name
            self.option_type: str = option_type
            self.current_option: int = 0
            self.text: str = text
            self.options: list[str] = options
            self.exec: partial[str] = exec

        def __str__(self) -> str:
            """Returns self.text formatted with the corresponding value from
            the config dict if appropriate.
            """
            if config is not None and config.get(self.name) is not None:
                return self.text.format(
                    value=cast(str, config.get(self.name)).replace("_", " "))
            return self.text

        def toggle(self) -> None:
            """Switch to "True" or "False" the corresponding config entry
            if the Option object is of type "toggle".
            """
            if config[self.name] == "True":
                config[self.name] = "False"
            else:
                config[self.name] = "True"

        def value_up(self, factor: int) -> None:
            """Handles the modification of slider values upward, checking
            if the upper limit is reached and updating the corresponding
            config entry accordingly.
            """
            value_range: range
            if self.option_type == "slider":
                value: int = int(config[self.name])
                value += factor
                value_range = cast(range, get_config_ranges(self.name))
                if value > value_range[-1]:
                    value = value_range[0]
                config[self.name] = str(value)
            elif self.option_type == "double_slider":
                values: list[int] = [
                    int(config[self.name].split(",")[0]),
                    int(config[self.name].split(",")[1])]
                values[self.current_option] += factor
                value_range = cast(
                    range, get_config_ranges(self.name)[self.current_option])
                if values[self.current_option] > value_range[-1]:
                    values[self.current_option] = value_range[0]
                config[self.name] = ",".join(
                    [str(value) for value in values])

        def value_down(self, factor: int) -> None:
            """Handles the modification of slider values downward, checking
            if the upper limit is reached and updating the corresponding
            config entry accordingly.
            """
            value_range: range
            if self.option_type == "slider":
                value: int = int(config[self.name])
                value -= factor
                value_range = cast(range, get_config_ranges(self.name))
                if value < value_range[0]:
                    value = value_range[-1]
                config[self.name] = str(value)
            elif self.option_type == "double_slider":
                values: list[int] = [
                    int(config[self.name].split(",")[0]),
                    int(config[self.name].split(",")[1])]
                values[self.current_option] -= factor
                value_range = cast(
                    range, get_config_ranges(self.name)[self.current_option])
                if values[self.current_option] < value_range[0]:
                    values[self.current_option] = value_range[-1]
                config[self.name] = ",".join(
                    [str(value) for value in values])

        def value_left(self) -> None:
            """Updates the pertinent config dict entry, either by calling
            value down for slider and double_slider option types,
            or switching the selected value for selection option type.
            """
            if self.option_type in ("slider, double_slider"):
                self.value_down(10)
            elif self.option_type == "selection":
                config[self.name] = self.options[
                    self.options.index(config[self.name]) - 1]

        def value_right(self) -> None:
            """Updates the pertinent config dict entry, either by calling
            value up for slider and double_slider option types,
            or switching the selected value for selection option type.
            """
            if self.option_type in ("slider, double_slider"):
                self.value_up(10)
            elif self.option_type == "selection":
                config[self.name] = self.options[
                    (self.options.index(config[self.name]) + 1)
                    % len(self.options)]

        def browse_option(self, user_input: str) -> None:
            """Takes the user_input to handle navigating option by option.
            For directions, calls the associated method, and for
            confirm, calls toggle method or reinitialize the current_option
            nonlocal string.
            """
            if user_input in Keyboard.DOWN.value:
                self.value_down(1)
            elif user_input in Keyboard.UP.value:
                self.value_up(1)
            elif user_input in Keyboard.LEFT.value:
                self.value_left()
            elif user_input in Keyboard.RIGHT.value:
                self.value_right()
            elif user_input in Keyboard.CONFIRM.value:
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
                name="show_path",
                option_type="toggle",
                text="Show found path: {value}"),
            Option(
                name="theme",
                option_type="selection",
                options=[theme.name.capitalize() for theme in Themes],
                text="Current theme: {value}"),
            Option(
                name="save maze",
                option_type="validate",
                text="Save maze to output file",
                exec=partial(lambda _: "save_maze", "")),
            Option(
                name="save config",
                option_type="validate",
                text="Save configuration to config.txt",
                exec=partial(lambda _: "save_config", "")),
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
                name="pattern",
                option_type="selection",
                options=[pattern.name.capitalize() for pattern in Patterns],
                text=f"{"Central pattern:":<22}""{value:>13}"),
            Option(
                name="gen_algorithm",
                option_type="selection",
                options=list(Maze.generation_algorithms),
                text=(
                    f"{"Generation algorithm:":<22}"
                    "{value:>13}")),
            Option(
                name="sol_algorithm",
                option_type="selection",
                options=list(MazeSolver.solving_algorithms),
                text=(
                    f"{"Solving algorithm:":<20}"
                    "{value:>15}")),
            Option(
                name="seed",
                option_type="slider",
                text=f"{"Generation seed:":<22}""{value:>13}"),
            Option(
                name="randomize seed",
                option_type="validate",
                text="Randomize seed",
                exec=partial(randomize_seed, "")),
            Option(
                name="output_file",
                option_type="validate",
                text=f"{'Output file:':<15}""{value:>20.20}",
                exec=partial(lambda _: "file_rename", "")),
            Option(
                name="gen_speed",
                option_type="slider",
                text=f"{"Generation speed:":<22}""{value:>13}"),
            Option(
                name="generate maze",
                option_type="validate",
                text="- Generate maze -",
                exec=partial(lambda _: "maze_gen", "")),
            Option(
                name="back",
                option_type="validate",
                text="return",
                exec=partial(change_menu, "main"))],
    }

    def browse_menu(user_input: str) -> str:
        """Takes the user input as argument.

        Updates menues current informations depending on the pressed key
        to navigate menues and pass on the input to an Option object
        browse method if necessary.

        Returns a string corresponding to the execution function of
        validate Options.
        """
        nonlocal current_index
        nonlocal current_menu
        nonlocal focused_option
        if user_input in Keyboard.ESCAPE.value:
            if focused_option is not None:
                focused_option = None
            elif current_menu != "main":
                current_menu = "main"
                current_index = 0
        elif focused_option is not None:
            focused_option.browse_option(user_input)
        elif user_input in Keyboard.DOWN.value:
            current_index += 1
            if current_index > len(menues[current_menu]) - 1:
                current_index = 0
        elif user_input in Keyboard.UP.value:
            current_index -= 1
            if current_index < 0:
                current_index = len(menues[current_menu]) - 1
        elif user_input in Keyboard.CONFIRM.value:
            if menues[current_menu][current_index].option_type == "validate":
                return menues[current_menu][current_index].exec()
            elif menues[current_menu][current_index].option_type == "toggle":
                menues[current_menu][current_index].toggle()
            else:
                focused_option = menues[current_menu][current_index]
        return ""

    def print_menu(theme: Theme) -> None:
        """Displays the current menu, navigation index and errors applying
        the selected theme.
        """
        menu_width: int = max(
            len(str(entry)) for entry in chain(
                menues[current_menu], current_error.split("\n"))) + 6
        justify_menues: int = int(config_save["width"])
        window_size: terminal_size = get_terminal_size()
        if (
                int(config_save["width"]) * 4 > window_size.columns
                or int(config_save["height"]) * 2 > window_size.lines):
            justify_menues = 10
        quote: str = (
            "A labyrinth is not a place to be lost, but a path to be found.")
        if len(quote) > justify_menues * 4 + 1:
            style_print(
                theme.walls_style,
                quote[:38].center(justify_menues * 4 + 1), "\n")
            style_print(
                theme.walls_style,
                quote[39:].center(justify_menues * 4 + 1), "\n")
        else:
            style_print(
                theme.walls_style,
                quote.center(justify_menues * 4 + 1), "\n")
        print(CursorOperations.LIGHT_CLEAR, end="")
        line: str = (
            theme.angles.TOP_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.TOP_RIGHT)
        style_print(theme.walls_style, line.center(
            justify_menues * 4 + 1), "\n")
        for index, entry in enumerate(menues[current_menu]):
            if index == len(menues[current_menu]) - 1 and current_error == "":
                style_print(theme.walls_style, (
                    f"{theme.walls.VERTICAL}{" " * menu_width}"
                    f"{theme.walls.VERTICAL}").center(
                        justify_menues * 4 + 1),
                    "\n")
            elif index == len(menues[current_menu]) - 1:
                for errors in current_error.split("\n"):
                    style_print(
                        theme.walls_style, theme.walls.VERTICAL.rjust(int((int(
                            config_save["width"]) * 4 - menu_width) / 2 + 1)))
                    print_error(errors.center(menu_width),  end="")
                    style_print(theme.walls_style, theme.walls.VERTICAL, "\n")
            if index == current_index:
                line = (
                    ("\033[4m" if focused_option == entry else "")
                    + (
                        f"{SmallIcons.LEFT_ARROW} {entry} "
                        f"{SmallIcons.RIGHT_ARROW}").center(menu_width))
            else:
                line = (str(entry).center(menu_width))
            style_print(
                theme.walls_style, theme.walls.VERTICAL.rjust(
                    int((justify_menues * 4 - menu_width) / 2 + 1)))
            style_print(
                theme.walls_style, line.center(menu_width))
            style_print(theme.walls_style, theme.walls.VERTICAL.ljust(
                    int((justify_menues * 4 - menu_width + 1) / 2)),
                    "\n")
        line = (
            theme.angles.BOTTOM_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.BOTTOM_RIGHT)
        style_print(theme.walls_style, line.center(
            justify_menues * 4 + 1), "\n")

    def menues_module(
            current_action: str, user_input: str) -> str:
        """Function returned by the instantiate function, handling the
        selected action and user input to browse, display and update
        menues.
        """
        if current_action == "browse_menu":
            return browse_menu(user_input)
        elif current_action == "print_menu":
            print_menu(get_theme(config["theme"]))
        elif current_action == "maze_error":
            nonlocal current_error
            current_error = user_input
        elif current_action == "back_to_main":
            for key, value in config.items():
                config_save[key] = value
            change_menu("main")
        return ""

    return menues_module
