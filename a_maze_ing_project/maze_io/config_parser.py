
from random import randint
from a_maze_ing_project.maze_display import Patterns, Themes
from a_maze_ing_project.maze_solve import MazeSolver


def parse_config_file(
        file_name: str, entries: dict[str, str],
        mandatory_values: tuple[str, ...]) -> str:
    """Receives a file_name to open, a config dict to update with found
    values, and a list of said values names.

    Reads config file, ignoring empty lines and comments, and tries
    reading any line which would contain a Maze parameter.

    Returns a string containing either an error message or nothing.
    """
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
                    *mandatory_values,
                    "SEED", "PATTERN", "THEME", "GEN_SPEED"):
                error_message.append(
                    f" - unknown value key on line {number}: "
                    f"'{entry[0][:15]}={entry[1][:20]}'")
                continue
            entries.update({entry[0].lower(): entry[1]})
        else:
            error_message.append(
                f" - unknown entry on line {number}: '{line[:35]}'")
    return "\n".join(error_message)


def generate_config(
        config_file: str, config: dict[str, str],
        mandatory_values: tuple[str, ...]) -> str:
    """Exposed function of the parsing file. Receives a config file_name,
    a config dict to be updated with the parsed values, and their
    names in the mandatory list.

    Calls parsing config file function to get values written by the user
    and complement them with optional parameters with default values.

    Returns a string containing either an error message or nothing.

    Mandatory config values: WIDTH, HEIGHT, ENTRY, EXIT, PERFECT,
    GEN_ALGORITHM, IMPERFECT_ALGORITHM, SOL_ALGORITHM, OUTPUT_FILE

    Optional config values: SEED, PATTERN, THEME, GEN_SPEED
    """
    output: str = parse_config_file(config_file, config, mandatory_values)
    if output != "":
        return output
    try:
        if "seed" not in config.keys():
            config.update({"seed": str(randint(0, 1000000000000))})
        int(config["seed"])
        if config.get(
                "sol_algorithm", "None") not in MazeSolver.solving_algorithms:
            raise ValueError(
                "Unknown value attributed to sol_algorithm parameter, "
                "available: " + ", ".join(MazeSolver.solving_algorithms))
        patterns: list[str] = list(
            pattern.name.capitalize() for pattern in Patterns)
        if config.get("pattern", "None") not in patterns:
            raise ValueError(
                "Unknown value attributed to pattern parameter, available: "
                ", ".join(patterns))
        config.update({"pattern": config.get("pattern", "None")})
        themes: list[str] = list(
            theme.name.capitalize() for theme in Themes)
        if config.get("theme", "Default") not in themes:
            raise ValueError(
                "Unknown value attributed to theme parameter, available: "
                ", ".join(themes))
        config.update({"theme": config.get("theme", "Default")})
        if "gen_speed" not in config.keys():
            config.update({"gen_speed": "3"})
        if int(config["gen_speed"]) not in range(0, 11):
            raise ValueError(
                "Generation speed parameter must be an int between 0 and 10.")
    except ValueError as error:
        output = f"- {str(error)}"
    config.update({"show_path": "True"})
    return output
