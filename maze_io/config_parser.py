
from random import randint
from maze_display import Patterns
from maze_display import Themes


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
                    *mandatory_values, "SEED", "PATTERN", "THEME"):
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
    output: str = parse_config_file(config_file, config, mandatory_values)
    if output != "":
        return output
    try:
        if "seed" not in config.keys():
            config.update({"seed": str(randint(0, 1000000000000))})
        int(config["seed"])
        if config.get("pattern", "None").upper() not in (
                pattern.name for pattern in Patterns):
            raise ValueError("Unknown value attributed to pattern parameter.")
        config.update({"pattern": config.get("pattern", "None")})
        if config.get("theme", "Default").upper() not in (
                theme.name for theme in Themes):
            raise ValueError("Unknown value attributed to theme parameter.")
        config.update({"theme": config.get("theme", "Default")})
    except ValueError as error:
        output = f"- {str(error)}"
    config.update({"show_path": "True"})
    return output
