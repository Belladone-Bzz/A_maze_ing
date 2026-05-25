
def parse_config_file(
        file_name: str, entries: dict[str, str],
        mandatory_values: tuple[str, ...]) -> tuple[str, str]:
    print(f"Reading configuration from file {file_name}...")
    try:
        with open(file_name, 'r') as file:
            lines: list[str] = file.readlines()
    except FileNotFoundError:
        return (
            f" - File '{file_name}' was not found or does not exist",
            "")
    except PermissionError:
        return (
            f" - File '{file_name}' has access restrictions "
            + "and could not be read", "")
    error_message: list[str] = []
    output_file: str = ""
    for number, line in enumerate(lines):
        line = line.strip("\n")
        if line.startswith("#") or line == "":
            continue
        entry: list[str] = line.split("=")
        if len(entry) == 2:
            if entry[0] == "OUTPUT_FILE":
                output_file = entry[1]
                continue
            if entry[0] not in mandatory_values:
                error_message.append(
                    f" - unknown value key on line {number}: "
                    f"'{entry[0][:15]}={entry[1][:20]}'")
                continue
            entries.update({entry[0].lower(): entry[1]})
        else:
            error_message.append(
                f" - unknown entry on line {number}: '{line[:35]}'")
    if output_file == "":
        error_message.append(
            " - missing OUTPUT_FILE value in configuration file.")
    return ("\n".join(error_message), output_file)


def get_boolean(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    raise TypeError(
        f"invalid boolean value '{value}', must be 'True or 'False'")


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
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "SEED",
        "CENTRAL_ICON", "GEN_ALGORITHM")
    parsing_output: tuple[str, str] = parse_config_file(
        argv[1], config, mandatory_values)
    if parsing_output[0] != "":
        print_error(
            "\nOne or multiple errors caught during parsing of file "
            f"'{argv[1]}':\n{parsing_output[0]}")
        return 2
    from maze_gen import Maze
    from pydantic import ValidationError
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
        print_error(
            "\nOne or multiple errors caught during configuration reading:\n"
            f"{message}")
        return 3
    from time import sleep
    from maze_display import print_maze, print_interface, get_themes
    input(
        "\nCorrect configuration found and loaded."
        "\nStarting A_maze_ing program... ⏎ ")
    menues: dict[str, tuple[str] | dict[str, str | tuple[str]]] = {
        "main": (
            "Change current theme", "Show/Hide found path"
            "Generate new maze", "Quit A_maze_ing"),
        "maze config": {"Theme"}}
    menues
    if maze.config.WIDTH < 51 and maze.config.HEIGHT < 40:
        for _ in maze.stepped_generation():
            print_maze(maze, get_themes()["basic design"])
            sleep(0.01)
    print_interface(maze, get_themes()["basic design"])
    return 0


if __name__ == "__main__":
    exits: tuple[str, ...] = (
        "Success", "Not enough argument", "File parsing error",
        "Config parsing error", "Keyboard interrupt")
    output: int
    try:
        output = main()
    except KeyboardInterrupt:
        output = 4
    print(f"\rEnding program with code : {output} ({exits[output]})")
