
from maze_gen import Maze


def parse_config_file(
        file_name: str, entries: dict[str, str],
        mandatory_values: tuple[str, ...]) -> str:
    print(f"Reading configuration from file {file_name}...")
    try:
        with open(file_name, 'r') as file:
            lines: list[str] = file.readlines()
    except FileNotFoundError:
        return f" - File '{file_name}' was not found or does not exist"
    except PermissionError:
        return (
            f" - File '{file_name}' has access restrictions "
            "and could not be read")
    error_message: list[str] = []
    for number, line in enumerate(lines):
        line = line.strip("\n")
        if line.startswith("#") or line == "":
            continue
        entry: list[str] = line.split("=")
        if len(entry) == 2:
            if entry[0] not in (
                    *mandatory_values, "SEED", "CENTRAL_ICON", "THEME"):
                error_message.append(
                    f" - unknown value key on line {number}: "
                    f"'{entry[0][:15]}={entry[1][:20]}'")
                continue
            entries.update({entry[0].lower(): entry[1]})
        else:
            error_message.append(
                f" - unknown entry on line {number}: '{line[:35]}'")
    return "\n".join(error_message)


def get_boolean(value: str | bool) -> bool:
    if str(value) == "True":
        return True
    elif str(value) == "False":
        return False
    raise TypeError(
        f"invalid boolean value '{value}', must be 'True or 'False'")


def instantiate_maze(
        config: dict[str, str],
        mandatory_values: tuple[str, ...]) -> str | Maze:
    try:
        from pydantic import ValidationError
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


def write_out_maze(maze: Maze, config: dict[str, str]) -> str:
    maze_str: str = ""
    for y in range(maze.config.HEIGHT):
        for x in range(maze.config.WIDTH):
            maze_str += hex(int("".join([str(
                int(wall)) for wall in maze.cells[x][y].walls]), 2))[2].upper()
        maze_str += "\n"
    maze_str += f"\n{config["entry"]}\n{config["exit"]}\n"
    try:
        with open(config["output_file"], 'w') as file:
            print(maze_str, end="", file=file)
    except FileNotFoundError:
        return f"- Output file {config["output_file"]} not found"
    except PermissionError:
        return f"- Output file {config["output_file"]} could not be accessed"
    return ""


def main() -> int:
    from sys import argv
    from maze_display import print_error
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
    parsing_output: str = parse_config_file(
        argv[1], config, mandatory_values)
    if parsing_output != "":
        print_error(
            "\nOne or multiple errors caught during parsing of file "
            f"'{argv[1]}':\n{parsing_output}")
        return 2

    from random import randint
    try:
        if "seed" not in config.keys():
            config.update({"seed": str(randint(0, 1000000000000))})
        int(config["seed"])
        if config.get("central_icon", "True") not in ("True", "False"):
            raise ValueError
        config.update({"central_icon": config.get("central_icon", "True")})
        if config.get("theme", "Default") not in (
                "Default", "Bees", "Metamorphosis"):
            raise ValueError
        config.update({"theme": config.get("theme", "Default")})
    except ValueError as error:
        print_error("\nOne or multiple errors caught during reading of"
                    "optional configuration values:\n" + str(error))
    config.update({"show_path": "True"})

    maze: str | Maze = instantiate_maze(config, mandatory_values)
    if isinstance(maze, str):
        print_error(
            "\nOne or multiple errors caught during configuration reading:\n"
            + maze)
        return 3
    from collections.abc import Callable
    from terminedia import getch
    from maze_display import (
        print_maze, Theme, get_themes, print_maze_generation,
        instantiate_menues)
    input(
        "\nCorrect configuration found and loaded."
        "\nStarting A_maze_ing program... ⏎ ")
    user_input: str
    menu_output: str
    menu_module: Callable[[str, str | Theme], str]
    while True:
        print_maze_generation(maze, get_themes()[config["theme"]])
        menu_module = instantiate_menues(config)
        while True:
            if maze.config.WIDTH < 51 and maze.config.HEIGHT < 40:
                print_maze(maze, get_themes()[config["theme"]])
            else:
                print("too small")
            menu_module("print_menu", get_themes()[config["theme"]])
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
            elif menu_output == "save_maze":
                menu_output = write_out_maze(maze, config)
                if menu_output != "":
                    menu_module("maze_error", menu_output)
    return 0


if __name__ == "__main__":
    exits: tuple[str, ...] = (
        "Success", "Not enough argument", "File parsing error",
        "Config parsing error", "Keyboard interrupt")
    from maze_display import ProgramQuit
    output: int
    try:
        output = main()
    except KeyboardInterrupt:
        output = 4
    except ProgramQuit:
        output = 0
    print(f"\rEnding program with code : {output} ({exits[output]})")
