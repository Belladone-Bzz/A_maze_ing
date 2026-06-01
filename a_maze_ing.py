
from maze_gen import Maze
from maze_io import write_out_maze, generate_config, get_boolean
from pydantic import ValidationError
from sys import argv, stdin
from os import name
from typing import cast
from collections.abc import Callable
from maze_display import (
    print_error, print_maze, Theme, get_themes, print_maze_generation,
    instantiate_menues, ProgramQuit)


if name != "nt":
    from termios import (
        tcgetattr, tcsetattr, ICANON, ECHO, TCSAFLUSH)
    from atexit import register
    fd: int = stdin.fileno()
    new_term: list[int | list[int]] = tcgetattr(fd)
    old_term: list[int | list[int]] = tcgetattr(fd)
    new_term[3] = (cast(int, new_term[3]) & ~ICANON & ~ECHO)
    tcsetattr(fd, TCSAFLUSH, new_term)

    def set_normal_term() -> None:
        tcsetattr(fd, TCSAFLUSH, old_term)
    register(set_normal_term)
else:
    try:
        from msvcrt import getch
    except (ImportError, AttributeError):
        print_error(
            "A_maze_ing program error:\n - msvcrt.getch could not be imported "
            "from your python package.")


def instantiate_maze(
        config: dict[str, str],
        mandatory_values: tuple[str, ...]) -> str | Maze:
    try:
        maze = Maze(
            width=int(config["width"]),
            height=int(config["height"]),
            entry=(
                int(config["entry"].split(",")[0]),
                int(config["entry"].split(",")[1])),
            exit=(
                int(config["exit"].split(",")[0]),
                int(config["exit"].split(",")[1])),
            perfect=get_boolean(config["perfect"]),
            gen_algorithm=config["gen_algorithm"],
            seed=int(config["seed"]),
            central_icon=get_boolean(config["central_icon"]))
        return maze
    except (KeyError, TypeError, IndexError,
            ValueError, ValidationError) as error:
        message: str
        if isinstance(error, ValidationError):
            message = "\n".join(f" - {e["msg"]}" for e in error.errors())
        elif isinstance(error, KeyError):
            message = (
                " - Missing configuration mandatory values: "
                f"{", ".join(
                    missing for missing in mandatory_values
                    if missing.lower() not in config.keys())}")
        else:
            message = f" - {error}"
        return message


def main() -> int:
    if len(argv) != 2:
        print_error(
            "\nIncorrect number of argument; execute the program using "
            "the syntax:\n - python a_maze_ing.py <text file containing "
            "maze configuration>")
        return 1

    config: dict[str, str] = {}
    mandatory_values: tuple[str, ...] = (
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "GEN_ALGORITHM",
        "SOL_ALGORITHM", "OUTPUT_FILE")
    parsing_output: str = generate_config(
        argv[1], config, mandatory_values)
    if parsing_output != "":
        print_error(
            "\nOne or multiple errors caught during parsing of file "
            f"'{argv[1]}':\n{parsing_output}")
        return 2

    maze: str | Maze = instantiate_maze(config, mandatory_values)
    if isinstance(maze, str):
        print_error(
            "\nOne or multiple errors caught during configuration reading:\n"
            + maze)
        return 3

    input(
        "\nCorrect configuration found and loaded. "
        "Starting A_maze_ing program... ⏎ ")
    user_input: str
    menu_output: str
    menu_module: Callable[[str, str | Theme], str] = instantiate_menues(config)
    themes: dict[str, Theme] = get_themes()
    while True:
        print_maze_generation(maze, themes[config["theme"]])
        while True:
            if maze.config.WIDTH < 51 and maze.config.HEIGHT < 40:
                print_maze(maze, themes[config["theme"]])
            else:
                print("too small")
            menu_module("print_menu", themes[config["theme"]])
            if name != "nt":
                user_input = stdin.read(1)
                if user_input == "\x1b" and stdin.read(1) == "[":
                    user_input = stdin.read(1)
                else:
                    user_input = user_input.lower()
            else:
                user_input = getch()
            menu_output = menu_module("browse_menu", user_input)
            if menu_output == "maze_gen":
                new_maze: str | Maze = instantiate_maze(
                    config, mandatory_values)
                if isinstance(new_maze, str):
                    menu_module("maze_error", new_maze)
                else:
                    maze = new_maze
                    break
            elif menu_output == "file_rename":
                if name != "nt":
                    tcsetattr(fd, TCSAFLUSH, old_term)
                config["output_file"] = input(
                    "Enter new file name for maze output: ")
                if name != "nt":
                    tcsetattr(fd, TCSAFLUSH, new_term)
            elif menu_output == "save_maze":
                menu_output = write_out_maze(maze, config)
                if menu_output != "":
                    menu_module("maze_error", menu_output)
    return 0


if __name__ == "__main__":
    output: int
    try:
        output = main()
    except KeyboardInterrupt:
        output = 4
    except ProgramQuit:
        output = 0
    exits: tuple[str, ...] = (
        "Success", "Not enough argument", "File parsing error",
        "Config parsing error", "Keyboard interrupt")
    print(f"\r\nEnding program with code : {output} ({exits[output]})")
