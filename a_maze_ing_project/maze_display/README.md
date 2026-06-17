# A_maze_ing

## Maze_display module

This module is responsible of every printing methods and algorithms, as well as containing all Enum classes related to special characters, style printing and cursor manipulations. Both [display](#display.py) and [menues](#menues.py) files are accessible through a single enclosing function[^closure] that manages the states of the Maze and its config, while [themes](#themes.py) and [utils](#utils.py) contains constants variables. This latter utility file can be found as a [Github Gist here](https://gist.github.com/jolyne-mangeot/895674d11a3ae2783075051bd6fdaf95).

### display.py

#### Functions:

- `instantiate_maze_display(config: dict[str, str]) -> Callable[[str, Maze, MazeSolver], None]`: Exposed function of the display file, enclosing all other functions so they all can keep track of the currently selected theme within the `current_theme` variable through the config dict given as argument. It returns `maze_display`.

- `calculate_intersection_index(bin_bool: tuple[bool, bool, bool, bool]) -> int:` Transforms 4 booleans designed to be walls to find which intersection character to use by returning an index between 0 and 15.

- `print_maze(maze: Maze, theme: Theme, solver: MazeSolver) -> None:`: Displays the maze cell by cell, surrounding them with special characters depending on which of their walls are open or not. Displays each angle based on open walls, outputting an adaptive and clear display depending on the theme argument containing characters and styles to print. Uses the MazeSolver object to display Shade Enum characters if cells are `visited`, `highlighted` or part of the found `path`.

- `get_fill_character(cell_1: CellCoordinates, movement: Movements | None = None) -> str:`: function nested into `print_maze` checking if a cell or its separation with another should be filled with block characters to signify a `visited`, `highlighted` or in `path` state.

- `integrate_entry_exit(maze: Maze, theme: Theme) -> None`: Function called after `print_maze`, going back on the print to integrate the icons for the entry and the exit coordinates with their corresponding styling.

- `integrate_pattern_design(maze: Maze, theme: Theme) -> None`: Function called after `print_maze`, going back on the print to integrate the selected pattern design. Works with the [CursorOperations enum](#Enums-2), and takes a Maze object as argument.

- `integrate_found_path(theme: Theme, path: list[CellCoordinates]) -> None`:Function called after print_maze, going back on the print to integrate the solver's found path. Works with nested functions get_line_character and add_cell_separation to integrate the selected theme's characters and styling for the path.

- `display_maze(maze: Maze, theme: Theme, solver: MazeSolver) -> None`: This is the function called when displaying the Maze's interface. It checks with the termios[^termios] module the size of the current terminal and calls the `print_maze` function when possible.

- `display_maze_generation(maze: Maze) -> None`: Works the same as `display_maze`, but it responsible of calling the `stepped_generation` Maze generator method to call `print_maze` every time a new cell is accessed. If the terminal is too small, or the `gen_speed` config parameter if 0, the `generate_maze` Maze method is called instead to skip the generator yields[^generator].

- `display_maze_solving(maze: Maze, theme: Theme, solver: MazeSolver) -> None`: Works the same as `display_maze_generation` to call the solver's stepped or instant solving algorithm and displaying the maze each time the stepped method yields None.

- `maze_display(current_display: str, maze: Maze, solver: MazeSolver) -> None`:  This function is the one returned by the enclosing `instantiate_maze_display`. It takes a current display string and a Maze, and recovers the selected theme through the `config` nonlocal dict. The three possible displays are 'display_maze', 'display_maze_generation' and 'display_maze_solving'.

> [!NOTE]
> Both the print_maze and integrate_pattern_design use a binary indexing to chose which intersection character to use. With each cell intersection consisting of 16 possibilities, the corresponding character to print depends on a tuple of boolean of which cell is accessible or not joined as a string of binary and converted to decimal.

### menues.py

#### Classes:

- `ProgramQuit(Exception)`: Exception raised when option 'quit program' is selected through execution function.

- `Options`: This class is enclosed in the later described `instantiate_menues` function to gain access to its nonlocal variables. It takes various string, list of strings and sometimes an execution function to handle different type of menu options. Takes a mandatory `name`, `option_type` and `text` string arguments to init, while `options` and `exec` are only necessary to 'selection' and 'validation' option types respectively. Has access to the following instances methods:

	- `toggle(self) -> None`: Switches to "True" or "False" the corresponding config entry if the option type of the object is 'toggle'.
	- `value_up(self, factor: int) -> None`: Handles the modification of 'slider' and 'double_slider' values upward by the factor argument, checking if the upper limit is reached and updating the corresponding config entry accordingly.
	- `value_down(self, factor: int) -> None`: Same as `value_up`
	- `value_left(self) -> None`: Updates the pertinent config dict entry, either by calling value down for slider and double_slider option types, or switching the selected value for selection option type.
	- `value_right(self) -> None`: Same as `value_left`
	- `browse_option(self, user_input: str) -> None`: Takes the user_input to handle navigating option by option. For directions, calls the associated method, and for confirm, calls toggle method or reinitialize the current_option nonlocal string.

#### Functions:

- `instantiate_menues(config: dict[str, str]) -> Callable[[str, str], str]`: This function is the only exposed callable of this file, enclosing all needed functions, variables and class ([Options](#Classes)) to render and navigate the Maze's menues. It takes as argument the config dict containing the values as strings used by the A_maze_ing program to instantiate maze and updates it with the user's new values. Works with the following nonlocal attributes:
`config_save: dict[str, str]` `current_menu: str` `current_index: int` `current_error: str ` `focused_option: "Option" | None ` and an Options objects-instantiating dict `menues: dict[str, list[Option]]`.

- `get_config_ranges(option: str) -> range | tuple[range, range]`: is a utility function returning range of possible values for each 'slider' (numeric value through which the user can scroll through the menues) depending on config or pre-set values, or a tuple of ranges for 'double_sliders', used for the user to enter coordinates. The option argument is here always the `name` attribute of an Option object.

- `change_menu(new_menu: str) -> str`: Execution function used to navigate to a new menu, updating the `current_menu` nonlocal string with the menu given as argument. If the user enters or leaves the maze_config menu, the config_save dict is used to update or updated with the config dict.

- `leave_program(_: str) -> str`: Execution function called to raise ProgramQuit Exception.

- `randomize_seed(_: str) -> str`: Execution function called to randomize the Maze config's seed.

- `browse_menu(user_input: str) -> str`: Updates nonlocal variables depending on the pressed key to navigate menues and pass on the input to an Option object browse method if necessary. Does so by comparing the user_input string passed as argument with values from the [Keyboard Enum](#Enums)

- `print_menu(theme: Theme) -> None`: Displays the current menu, navigation index and errors applying a theme recovered from the config dict.

- `menues_module(current_action: str, user_input: str) -> str`: This function is the one returned by the enclosing `instantiate_menues` functio. It takes an action to perform and an input, transferring the latter one to the subsequently called function depending on the action. Actions possible and their associated code:

	- "browse_menu": `browse_menu()`
	- "print_menu": `print_menu()`
	- "maze_error": updates the `current_error` nonlocal string with the input.
	- "back_to_main": Manually calls `change_menu("main")` and updates the `config_save` enclosed dict with the current config. Used when successfully generating a maze.

> [!NOTE]
> What are called execution functions are the callable passed as argument to Option objects for their optional `exec` attribute. They therefore have to respect the same typing, taking as parameter and returning strings.

### themes.py

#### Classes:

- `Theme`: This class works as a template for all caracteristics needed to make up the Maze's display with characters Enums for walls, angles and the pattern, and stylings for each of them. No verification are made during instantiation, examples of objects are declared in the following Enum.

#### Enums:

- `Themes(Enum)`: Enumeration of different set Theme objects to be used by the Maze and menues displays in our A_maze_ing program.

- `Patterns(Enum)`: The Pattern enumeration is stored upmost in the file, taking the shape of tuple of tuple of `0`s and `1`s. These are the lines that make up the patterns to add to the final Maze, `1` being where a cell is part of the pattern, and `0` are the free cells. To print out the Maze and its pattern with each their own style, it is better to directly use the Patterns here as, when the Maze generates itself, it also marks the enclosed free cells as part of the pattern as to not take them into account when breaking random walls to make itself an imperfect maze.

#### Functions:

- `get_theme(theme: str) -> Theme`: This function returns the Theme object linked to the Enum key passed in arguments. As Enum classes cannot be accessed by key like dictionaries, it uses the `getattr` function. Does no verification of a pre-existing entry in the Themes Enum by the name of the argument as this function is only ever called by the program, and the user theme selection depends on a set list consisting of the Themes Enum keys.

### utils.py

The utils file of this module's purpose is to make one's job of printing out information into the terminal as simple as possible while maintaining a light code and satisfactory outputs. It groups special characters in classes, style, color and cursor manipulation codes and essential functions to make it all work together.

#### Classes:

- `Walls`: The wall class is here to group in type all inheriting wall classes that will store the 7 special characters[^box_chars] to make up the Maze's borders. It so contains the declared but undefined attributes: `VERTICAL` `HORIZONTAL` `VERTICAL_R` `VERTICAL_L` `HORIZONTAL_U` `HORIZONTAL_D` `CROSS` `DOT`. With every child class assigning values to these variables, they will then be usable by the Maze and menues printing functions, with the following walls added:

	- `BasicWalls`: `│` `─` `├` `┤` `┴` `┬` `┼` `·`
	- `BoldBasicWalls`: `┃` `━` `┣` `┫` `┻` `┳` `╋` `•`
	- `DoubleWalls`: `║` `═` `╠` `╣` `╩` `╦` `╬` `◦`

- `Angles`: This class works the same as Walls, but concerns angle Unicode characters. The following 4 attributes are declared here: `TOP_LEFT` `TOP_RIGHT` `BOTTOM_LEFT` `BOTTOM_RIGHT`, and assigned values in the following children classes:

	- `BasicAngles`: `┌` `┐` `└` `┘`
	- `BoldBasicAngles`: `┏` `┓` `┗` `┛`
	- `DoubleAngles`: `╔` `╗` `╚` `╝`
	- `RoundedAngles`: `╭` `╮` `╰` `╯`

> [!NOTE]
> These 2 class families were originally declared as Enum's, but the problem of group typing was faced as the entire class had to be given out as argument, rather than each character on its own, and no solution of inheritance or duck typing was found during the making of this project.

#### Enums:

- `Keyboard(Enum)`: Groups in tuples of strings possible user inputs as keys, for instance `w` and `\x1b[A` (arrow up) for `Keyboard.UP`.

- `StyleEnum(Enum)`: This Enum, destined to be inherited by styling related enumerations, only contains an override of the `__str__` method, returning its own value instead of name when a member of any StyleEnum is converted to a string (most notably when given to print functions).

- `Shades(StyleEnum)`: This Enum contains different shade characters for any and all purposes.

- `SmallIcons(StyleEnum)`: The SmallIcons enum is exposed in the maze_display module, and stores various special characters[^spe_chars] and emojis to make accessible wherever needed.

- `Colors(StyleEnum)`: This Enum stores as string the color code of various shades. These code are useful to insert into ASCII escape sequences. They do not correspond to the [8-16 basic sets of colors](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes), but the [256 color codes](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#256-colors) (for reference). In any case, they cannot be used on their own but must be inserted into the correct sequence syntax to have the expected result: `ESC[38;5;{code}m` (38 for foreground, 48 for background). In this module, they can be used with the later described style_print function, which inserts colors given as argument into a correct sequence to print out.

- `Styling(StyleEnum)`: The Styling enum members work relatively the same as Colors, with different terminal supporting different effects or not (blinking is not supported by VScode, for instance). The codes for the [basic text styling](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode) (bold, dim, italic, underlined, blinking) are stored in the enum, and they all must be inserted into a sequence to have an effect: `ESC[{code}m`

- `CursorOperations(StyleEnum)`: Finally, the CursorOperations are cursor manipulations extremely handy when printing multiple elements into a terminal at different times, keeping the display clean and gaining a lot of time and code clarity. Contrary to Colors and Styling, the strings stored here can be printed out on their own to take effect, their usage being much more applicable in any print. There are two operations categories:

	- [Cursor control](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#cursor-controls): Useful to move the cursor around cell by cell, line by line or even using coordinates, but also saving its position to restore it later.
	- [Erase functions](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#erase-functions): As in their name, that can erase lines, parts of lines, the entire terminal, etc. The style clearing code is also stored here, usable to restore the default display between prints to avoid styles transferring.

> [!NOTE]
> For more details on how the StyleEnum's are used in our project, this Github Gist here[^gist] was our main resource to compose what is called ASCII escape sequences[^ascii_code] to alter and enrich terminal printing and display. Useful as they are, this utils file is then made to be usable in as many project that need terminal printing as possible.

#### Functions:

- `move_cursor(y: int, x: int = 0) -> str`: This function is actually stored in the CursorOperation Enum, and uses the `ESC[{y};{x}H` ASCII code to place the cursor to a given position on the terminal display.

- `styling(style: list[Styling] = [], fg_color: Colors | str | int = Colors.DEFAULT, bg_color: Colors | str | int = Colors.DEFAULT) -> str`: The return of this styling function was thought out to be stored or directly printed with the style_print function. It makes from the passed Styling and Colors Enum values a custom 'theme' that can group as as many effects as one could want. For colors, the values can range from 0 to 255 and be inserted as value from the Colors enum, a string or an int of the values. No verification of range is made, feel free to experiment until the output style is to your liking (see Styling and Colors [Enums](#Enums-3) for more info).

- `style_print(style: str, content: str, end: str = "") -> None`: style_print is a single line function applying a theme to a string and printing it out. It can also print an end message, which is devoid of styling. The `sep` and `end` arguments of the print call are set to `""` to give out more control over the output.

- `print_error(content: str, end: str = "\n\nRefer to the provided README file for guidance.\n\n" ) -> None`: Uses both styling and style_print functions to print out a message in bold red with a set overwritable end message.

## Resources

> [!NOTE]
> No AI was used in the making of this module nor README file. Documentation written by [jolyne-mangeot](https://github.com/jolyne-mangeot)

[^closure]: [Function closures in python](https://dev.to/m16bappi/understanding-closures-in-python-4mdi)

[^termios]: [Termios module documentation](https://docs.python.org/3.13/library/termios.html)

[^generator]: [Generators documentation](https://www.w3schools.com/python/python_generators.asp)

[^box_chars]: [Wikipedia list of box drawing character](https://en.wikipedia.org/wiki/Box-drawing_characters)

[^spe_chars]: [Wikipedia list of unicode characters](https://en.wikipedia.org/wiki/List_of_Unicode_characters)

[^gist]: [Github Gist by fnky](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)

[^ascii_code]: [Wikipedia page on escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
