# A_maze_ing

## Maze_display module

### display.py


### menues.py


### themes.py

#### Enums:

- `Patterns(Enum)`: The Pattern enumeration is stored upmost in the file, taking the shape of tuple of tuple of `0`s and `1`s. These are the lines that make up the patterns to add to the final Maze, `1` being where a cell is part of the pattern, and `0` are the free cells. To print out the Maze and its pattern with each their own style, it is better to directly use the Patterns here as, when the Maze generates itself, it also marks the enclosed free cells as part of the pattern as to not take them into account when breaking random walls to make itself an imperfect maze.


### utils.py

The utils file of this module's purpose is to make one's job of printing out information into the terminal as simple as possible while maintaining a light code and satisfactory outputs. It groups special characters in classes, style, color and cursor manipulation codes and essential functions to make it all work together.

#### Classes:

- `Walls`: The wall class is here to group in type all inheriting wall classes that will store the 7 [special characters](https://en.wikipedia.org/wiki/List_of_Unicode_characters#Box_Drawing) to make up the Maze's borders. It so contains the declared but undefined attributes: `VERTICAL` `HORIZONTAL` `VERTICAL_R` `VERTICAL_L` `HORIZONTAL_U` `HORIZONTAL_D` `CROSS`. With every child class assigning values to these variables, they will then be usable by the Maze and menues printing functions, with the following walls added:

	- `BasicWalls`: `│` `─` `├` `┤` `┴` `┬` `┼`
	- `BoldBasicWalls`: `┃` `━` `┣` `┫` `┻` `┳` `╋`
	- `DoubleWalls`: `║` `═` `╠` `╣` `╩` `╦` `╬`

- `Angles`: This class works the same as Walls, but concerns angle Unicode characters. The following 4 attributes are declared here: `TOP_LEFT` `TOP_RIGHT` `BOTTOM_LEFT` `BOTTOM_RIGHT`, and assigned values in the following children classes:

	- `BasicAngles`: `┌` `┐` `└` `┘`
	- `BoldBasicAngles`: `┏` `┓` `┗` `┛`
	- `DoubleAngles`: `╔` `╗` `╚` `╝`
	- `RoundedAngles`: `╭` `╮` `╰` `╯`

These 2 class families were originally declared as Enum's, but the problem of group typing was faced as the entire class had to be given out as argument, rather than each character on its own, and no solution of inheritance or duck typing was found during the making of this project.

#### Enums:

- `StyleEnum(Enum)`: This Enum, destined to be inherited by styling related enumerations, only contains an override of the `__str__` method, returning its own value instead of name when a member of any StyleEnum is converted to a string (most notably when given to print functions).

- `SmallIcons(StyleEnum)`: The SmallIcons enum is exposed in the maze_display module, and stores various special characters and emojis to make accessible wherever needed.

- `Colors(StyleEnum)`: This Enum stores as string the color code of various shades. These code are useful to insert into ASCII escape sequences. They do not correspond to the [8-16 basic sets of colors](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#color-codes), but the [256 color codes](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#256-colors) (for reference). In any case, they cannot be used on their own but must be inserted into the correct sequence syntax to have the expected result: `ESC[38;5;{code}m` (38 for foreground, 48 for background). In this module, they can be used with the later described style_print function, which inserts colors given as argument into a correct sequence to print out.

- `Styling(StyleEnum)`: The Styling enum members work relatively the same as Colors, with different terminal supporting different effects or not (blinking is not supported by VScode, for instance). The codes for the [basic text styling](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#colors--graphics-mode) (bold, dim, italic, underlined, blinking) are stored in the enum, and they all must be inserted into a sequence to have an effect: `ESC[{code}m`

- `CursorOperations(StyleEnum)`: Finally, the CursorOperations are cursor manipulations extremely handy when printing multiple elements into a terminal at different times, keeping the display clean and gaining a lot of time and code clarity. Contrary to Colors and Styling, the strings stored here can be printed out on their own to take effect, their usage being much more applicable in any print. There are two operations categories:

	- [Cursor control](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#cursor-controls): Useful to move the cursor around cell by cell, line by line or even using coordinates, but also saving its position to restore it later.
	- [Erase functions](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#erase-functions): As in their name, that can erase lines, parts of lines, the entire terminal, etc. The style clearing code is also stored here, usable to restore the default display between prints to avoid styles transferring.

For more details on how the StyleEnum's are used in our project, this [Github Gist here](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#ansi-escape-sequences) was our main resource to compose what is called [ASCII escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code) to alter and enrich terminal printing and display. Useful as they are, this utils file is then made to be usable in as many project that need terminal printing as possible.

#### Functions:

- `move_cursor(y: int, x: int = 0) -> str`: This function is actually stored in the CursorOperation Enum, and uses the `ESC[{y};{x}H` ASCII code to place the cursor to a given position on the terminal display.

- `styling(style: list[Styling] = [], fg_color: Colors | str | int = Colors.DEFAULT, bg_color: Colors | str | int = Colors.DEFAULT) -> str`: The return of this styling function was thought out to be stored or directly printed with the style_print function. It makes from the passed Styling and Colors Enum values a custom 'theme' that can group as as many effects as one could want. For colors, the values can range from 0 to 255 and be inserted as value from the Colors enum, a string or an int of the values. No verification of range is made, feel free to experiment until the output style is to your liking (see Styling and Colors [Enums](#Enums) for more info).

- `style_print(style: str, content: str, end: str = "") -> None`: style_print is a single line function applying a theme to a string and printing it out. It can also print an end message, which is devoid of styling. The `sep` and `end` arguments of the print call are set to `""` to give out more control over the output.

- `print_error(content: str, end: str = "\n\nRefer to the provided README file for guidance.\n\n" ) -> None`: Uses both styling and style_print functions to print out a message in bold red with a set overwritable end message.
