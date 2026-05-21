
def parse_config_file(
        file_name: str, entries: dict[str, str | int | bool | tuple[int, int]]
        ) -> tuple[bool, str]:
    print(f"Reading configuration from file {file_name}...\n")
    try:
        with open(file_name, 'r') as file:
            lines: list[str] = file.readlines()
    except FileNotFoundError:
        print(f"File {file_name} was not found or does not exist")
        return (True, "")
    except PermissionError:
        print(
            f"File {file_name} has access restrictions and could not be read")
        return (True, "")
    error: bool = False
    error_message: str = ""
    output_file: str = ""
    for line in lines:
        line = line.strip("\n")
        if line.startswith("#") or line == "":
            continue
        entry: list[str] = line.split("=")
        if len(entry) != 2:
            error_message +=\
                f"ERROR - Unknown entry in config file on line: {line[:25]}\n"
            error = True
        try:
            if entry[0] in ("HEIGHT", "WIDTH", "SEED"):
                entries.update({entry[0].lower(): int(entry[1])})
            elif entry[0] in ("PERFECT", "CENTRAL_ICON"):
                if entry[1] == "True":
                    entries.update({entry[0].lower(): True})
                elif entry[1] == "False":
                    entries.update({entry[0].lower(): False})
                else:
                    raise ValueError()
            elif entry[0] in ("ENTRY", "EXIT"):
                values: list[str] = entry[1].split(",")
                if len(values) != 2:
                    raise ValueError()
                entries.update({entry[0].lower(): (
                    int(values[0]), int(values[1]))})
            elif entry[0] in ("OUTPUT_FILE"):
                if entry[1] == "":
                    raise ValueError()
                output_file = entry[1]
            else:
                error_message +=\
                    f"ERROR - Unknown entry type {entry[0]} found\n"
                error = True
                continue
            if entry[0] != "OUTPUT_FILE":
                print(
                    f"{f"OK - Entry '{entry[0]}' saved with value":<42}",
                    f"- {entries[entry[0].lower()]}")
        except ValueError:
            error_message +=\
                f"{f"ERROR - Invalid value type for {entry[0]} entry:":<52}"\
                + f"- '{entry[1]}'\n"
            error = True
    print("\n", error_message, sep="", end="")
    return (error, output_file)


def main() -> int:
    from sys import argv
    if len(argv) != 2:
        print(
            "\nIncorrect number of argument;",
            "execute the program using the syntax:\n\n",
            "python a_maze_ing.py <text file containing maze configuration>")
        return 1
    config: dict[str, str | int | bool | tuple[int, int]] = {}
    parsing_output: tuple[bool, str] = parse_config_file(argv[1], config)
    if parsing_output[0] is True or parsing_output[1] == "":
        print(
            "\nOne or multiple errors brought up during parsing of file",
            f"'{argv[1]}'.\nRefer to the provided README file for guidance.")
        return 2
    from time import sleep
    from typing import cast
    from maze_gen import Maze
    from maze_display import print_maze, Theme, get_theme
    print(
        "Correct configuration found and loaded,"
        "starting A_maze_ing program...")
    # sleep(3)
    maze = Maze(
        width=cast(int, config["width"]),
        height=cast(int, config["height"]),
        entry=cast(tuple[int, int], config["entry"]),
        exit=cast(tuple[int, int], config["exit"]),
        perfect=cast(bool, config["perfect"]),
        seed=cast(int, config["seed"]),
        central_icon=cast(bool, config["central_icon"]))
    maze.generation()
    print(maze)

    print_maze(maze, get_theme("basic"))
    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Ending A_maze_ing program.")
