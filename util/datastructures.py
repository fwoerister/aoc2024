class Grid:
    def __init__(self, rows):
        self.rows = list(map(lambda line: list(line.strip()), filter(lambda x: x, rows)))
        self.height = len(self.rows)
        self.width = 0 if self.height == 0 else len(self.rows[0])

    def get_val_at(self, x: int, y: int) -> str:
        if self.is_on_grid(x, y):
            return self.rows[y][x]
        return None

    def set_val_at(self, x: int, y: int, val: object) -> None:
        if self.is_on_grid(x, y):
            self.rows[y][x] = val

    def is_on_grid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def foreach(self, func):
        for x in range(self.width):
            for y in range(self.height):
                func(x, y)

    def get_neighbours(self, x, y):
        neighbours = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        return list(filter(lambda n: self.is_on_grid(*n), neighbours))

    def get_horizontal_neighbours(self, x, y):
        neighbours = [
            (x + 1, y),
            (x - 1, y),
        ]

        return list(filter(lambda n: self.is_on_grid(*n), neighbours))

    def get_vertical_neighbours(self, x, y):
        neighbours = [
            (x, y + 1),
            (x, y - 1),
        ]

        return list(filter(lambda n: self.is_on_grid(*n), neighbours))

    def get_diagnoal_neighbours(self, x, y):
        neighbours = [
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
        ]

        return list(filter(lambda n: self.is_on_grid(*n), neighbours))

    def convert_to_int_vals(self):
        def convert_field_to_int(x: int, y: int) -> None:
            self.rows[y][x] = int(self.get_val_at(x, y))

        self.foreach(convert_field_to_int)

    def print_grid(self):
        for y in range(self.height):
            print(''.join(self.rows[y]))
        print()
