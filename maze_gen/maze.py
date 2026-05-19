from pydantic import BaseModel, Field, model_validator
from typing import Annotated


MazeDimension = Annotated[int, Field(ge=2)]
CellCoordinates = Annotated[
    tuple[
        Annotated[int, Field(ge=0)],
        Annotated[int, Field(ge=0)]],
    Field(min_length=2, max_length=2)]


class Maze:
    def __init__(
            self, width: int, height: int,
            entry: tuple[int, int], exit: tuple[int, int],
            perfect: bool, seed: int, central_icon: bool = False):
        self.config = Maze.Config(
            WIDTH=width,
            HEIGHT=height,
            ENTRY=entry,
            EXIT=exit,
            PERFECT=perfect,
            SEED=seed,
            CENTRAL_ICON=central_icon)

    class Config(BaseModel):
        WIDTH: MazeDimension
        HEIGHT: MazeDimension
        ENTRY: CellCoordinates
        EXIT: CellCoordinates

        CENTRAL_ICON: Annotated[bool, Field(default=False)]
        PERFECT: Annotated[bool, Field(default=True)]
        SEED: Annotated[int, Field()]

        @model_validator(mode='after')
        def validate_config(self) -> "Maze.Config":
            error_message: str = ""
            if self.CENTRAL_ICON is True and (
                    self.WIDTH < 7 or self.HEIGHT < 7):
                error_message +=\
                    "Generating a maze with dimensions inferior to 7 by 7 is "\
                    + "impossible when integrating the central pattern.\n"
            if self.ENTRY[0] >= self.HEIGHT or self.ENTRY[1] >= self.WIDTH:
                error_message +=\
                    "Entry coordinates (x, y)"\
                    + "cannot exceed the maze's dimensions\n"
            if self.EXIT[0] >= self.HEIGHT or self.EXIT[1] >= self.WIDTH:
                error_message +=\
                    "Exit coordinates (x, y)"\
                    + "cannot exceed the maze's dimensions\n"
            if error_message != "":
                raise ValueError(error_message)
            return self

        def __str__(self) -> str:
            return (
                f"WIDTH: {self.WIDTH}, HEIGHT: {self.HEIGHT}\n"
                f"ENTRY: {self.ENTRY}, EXIT: {self.EXIT}\n"
                f"ICON TOGGLE: {self.CENTRAL_ICON}, "
                f"PERFECT TOGGLE: {self.PERFECT}\nSEED: {self.SEED}")

    class Cell:
        pass


if __name__ == "__main__":
    config = Maze(
        width=2,
        height=2,
        entry=(0, 0),
        exit=(1, 1),
        perfect=True,
        seed=123456,
        central_icon=False
    )
    print(config.config)
