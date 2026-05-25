
def parse_config_file(
        file_name: str, entries: dict[str, str],
        mandatory_values: tuple[str, ...]) -> tuple[str, str]:
    print(f"Reading configuration from file {file_name}...")
    try:
        with open(file_name, 'r') as file:
            lines: list[str] = file.readlines()
    except FileNotFoundError:
        return (
            f" - File '{file_name}' was not found or does not exist\n",
            "")
    except PermissionError:
        return (
            f" - File '{file_name}' has access restrictions "
            + "and could not be read\n", "")
    error_message: str = ""
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
                error_message += (
                    f" - unknown value key on line {number}: "
                    f"'{entry[0][:15]}={entry[1][:20]}'\n")
                continue
            entries.update({entry[0].lower(): entry[1]})
        else:
            error_message +=\
                f" - unknown entry on line {number}: '{line[:35]}'\n"
    if output_file == "":
        error_message += (
        " - missing OUTPUT_FILE value in configuration file.\n")
    return (error_message, output_file)


def get_boolean(value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    raise TypeError(
        f"invalid boolean value '{value}', must be 'True or 'False'")


def main() -> int:
    from sys import argv
    if len(argv) != 2:
        print(
            "\nIncorrect number of argument;",
            "execute the program using the syntax:\n\n",
            "python a_maze_ing.py <text file containing maze configuration>")
        return 1
    config: dict[str, str] = {}
    mandatory_values: tuple[str, ...] = (
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "SEED",
        "CENTRAL_ICON", "GEN_ALGORITHM")
    parsing_output: tuple[str, str] = parse_config_file(
        argv[1], config, mandatory_values)
    if parsing_output[0] != "":
        print(
            "\nOne or multiple errors caught during parsing of file "
            f"'{argv[1]}':",
            parsing_output[0],
            "Refer to the provided README file for guidance.\n", sep="\n")
        exit()
    from pydantic import ValidationError
    from time import sleep
    from typing import cast
    from maze_gen import Maze
    from maze_display import print_maze, Theme, get_theme
    # sleep(3)
    try:
        maze = Maze(
            width=cast(int, int(config["width"])),
            height=cast(int, int(config["height"])),
            entry=cast(tuple[int, int], (int(config["entry"].split(",")[0]), int(config["entry"].split(",")[1]))),
            exit=cast(tuple[int, int], (int(config["exit"].split(",")[0]), int(config["exit"].split(",")[1]))),
            perfect=cast(bool, get_boolean(config["perfect"])),
            seed=cast(int, int(config["seed"])),
            central_icon=cast(bool, get_boolean(config["central_icon"])))
    except (KeyError, TypeError, IndexError,
            ValueError, ValidationError) as error:
        message: str
        if isinstance(error, ValidationError):
            message = "\n".join(f" - {e["msg"]}" for e in error.errors())
        elif isinstance(error, KeyError):
            message = (" - Missing configuration mandatory values: "
                f"{", ".join(
                    missing for missing in mandatory_values
                    if missing.lower() not in config.keys())}")
        else:
            message = f" - {error}"
        print(
            "\nOne or multiple errors caught during configuration reading:",
            message,
            "\nRefer to the provided README file for guidance.\n", sep="\n")
        exit()
    print(
        "Correct configuration found and loaded,",
        "starting A_maze_ing program...")

    maze.generation()
    maze.backtracking_algo()

    print_maze(maze, get_theme("basic"))
    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Ending A_maze_ing program.")
