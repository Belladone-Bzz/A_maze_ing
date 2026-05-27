
from .utils import style_print, SmallIcons
from maze_gen import CellCoordinates
from .themes import Theme
from typing import cast
from collections.abc import Callable
from functools import partial


class ProgramQuit(Exception):
    pass


def instantiate_menues(config: dict[str, str]
        ) -> Callable[[str, str | Theme], str | None]:

    current_menu: str = "main"
    current_index: int = 0

    def change_menu(new_menu: str) -> None:
        nonlocal current_menu
        nonlocal current_index
        current_menu = new_menu
        current_index = 0
        return ""

    def leave_program(_: str) -> None:
        print("Hihi !")
        raise ProgramQuit

    class Option:
        def __init__(
                self, name: str, option_type: str,
                text: str,
                value: str | bool | int | CellCoordinates | None = None,
                exec: Callable[[str], None] | None = None) -> None:
            self.name: str = name
            self.option_type: str = option_type
            self.text: str = text
            self.value: str | bool | int | CellCoordinates | None = value
            self.exec: Callable[[str], None] | None = exec

        def __str__(self) -> str:
            if self.value is not None:
                return self.text.format(self.value)
            return self.text

    menues: dict[str, list[Option]]
    menues = {
        "main": [
            Option(
                name="show path",
                option_type="toggle",
                value=True,
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
                name=,
                option_type=,
                value=,
                text=,
                exec=),
            {
                "name": "width", "option_type": "slider",
                "value": config["width"],
                "text": f"{"Width:":<22}{config["width"]:>13}"},
            {
                "name": "height", "option_type": "slider",
                "value": config["height"],
                "text": f"{"Height:":<22}{config["height"]:>13}"},
            {
                "name": "entry", "option_type": "slider",
                "value": config["entry"],
                "text": f"{"Entry:":<22}{config["entry"]:>13}"},
            {
                "name": "exit", "option_type": "slider",
                "value": config["exit"],
                "text": f"{"Exit:":<22}{config["exit"]:>13}"},
            {
                "name": "perfect", "option_type": "toggle",
                "value": config["perfect"],
                "text": f"{"Perfect:":<22}{config["perfect"]:>13}"},
            {
                "name": "central_icon", "option_type": "toggle",
                "value": config["central_icon"],
                "text": f"{"Central icon:":<22}{config["central_icon"]:>13}"},
            {
                "name": "gen_algorithm", "option_type": "selection",
                "options": ["Backtracking", "Prim"],
                "value": config["gen_algorithm"],
                "text": (
                    f"{"Generation algorithm:":<22}"
                    f"{config["gen_algorithm"]:>13}")},
            {
                "name": "sol_algorithm", "option_type": "selection",
                "options": ["Dijkstra"],
                "value": config["sol_algorithm"],
                "text": (
                    f"{"Solving algorithm:":<22}"
                    f"{config["sol_algorithm"]:>13}")},
            {
                "name": "seed", "option_type": "slider",
                "value": config["seed"],
                "text": f"{"Generation seed:":<22}{config["seed"]:>13}"},
            {
                "name": "randomize seed", "option_type": "validate",
                "text": "Randomize seed"},
            {
                "name": "output_file", "option_type": "text",
                "value": config["output_file"],
                "text": f"{"Output file:":<22}{config["output_file"]:>13}"},
            {
                "name": "generate maze", "option_type": "validate",
                "value": "True",
                "text": "- Generate maze -"},
            {
                "name": "back", "option_type": "validate", "text": "return",
                "exec": partial(change_menu, "main")}]}

    def update_text() -> None:
        menues["main"][0]["text"] = (
            ("Show" if menues["main"][0]["value"] is False else "Hide")
            + " found path")

    def browse_menu(user_input: str) -> str:
        nonlocal current_index
        nonlocal current_menu
        if user_input in ("s", "\x1b[B"):
            current_index += 1
            if current_index > len(menues[current_menu]) - 1:
                current_index = 0
        elif user_input in ("w", "\x1b[A"):
            current_index -= 1
            if current_index < 0:
                current_index =  len(menues[current_menu]) - 1
        elif user_input == "\r":
            if menues[current_menu][current_index].get(
                    "option_type") == "validate":
                return menues[current_menu][current_index].get("exec")()

    def print_menu(theme: Theme) -> None:
        nonlocal current_menu
        nonlocal current_index
        menu_width: int = max(
            len(entry["text"]) for entry in menues[current_menu]) + 6
        line: str = (
            theme.angles.TOP_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.TOP_RIGHT)
        style_print(
            theme.walls_style, line.center(int(config["width"]) * 4), "\n")
        for index, entry in enumerate(menues[current_menu]):
            if index == len(menues[current_menu]) - 1:
                style_print(theme.walls_style, (
                    f"{theme.walls.VERTICAL}{" " * menu_width}"
                    f"{theme.walls.VERTICAL}").center(int(config["width"]) * 4),
                    "\n")
            if index == current_index:
                line = ((
                    f"{SmallIcons.LEFT_ARROW} {entry["text"]} "
                    f"{SmallIcons.RIGHT_ARROW}").center(menu_width))
            else:
                line = (entry["text"].center(menu_width))
            style_print(
                theme.walls_style, theme.walls.VERTICAL.rjust(
                    int((int(config["width"]) * 4 - menu_width) / 2)))
            style_print(
                theme.icon_style, line.center(menu_width))
            style_print(theme.walls_style, theme.walls.VERTICAL, "\n")
        line: str = (
            theme.angles.BOTTOM_LEFT + (theme.walls.HORIZONTAL * menu_width)
            + theme.angles.BOTTOM_RIGHT)
        style_print(
            theme.walls_style, line.center(int(config["width"]) * 4), "\n")

    def menues_module(current_action: str, user_input: str | Theme) -> None:
        if current_action == "browse_menu":
            browse_menu(cast(str, user_input))
        elif current_action == "print_menu":
            print_menu(cast(Theme, user_input))

    return menues_module
