def count_walls(self) -> int:
	count: int = 0
	for y in range(0, (self.config.HEIGHT)):
		for x in range(0, (self.config.WIDTH)):
			if self.cells[x][y].walls[Directions.EAST] is True:
				count += 
			if self.cells[x][y].walls[Directions.SOUTH] is True:
				count += 1
	count -= (self.config.HEIGHT + self.config.WIDTH)
	return count


def is_imperfect(self) -> None:
	walls: int = (self.config.HEIGHT * self.config.WIDTH + 1) -\
	(self.config.HEIGHT + self.config.WIDTH)
	nb_to_destroy: int = int(walls/10)
	if nb_to_destroy == 0:
		nb_to_destroy += 1