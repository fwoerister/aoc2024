class Grid:
    def __init__(self, rows):
        self.rows = list(map(lambda line: list(line.strip()), filter(lambda x: x, rows)))
        self.height = len(self.rows)
        self.width = 0 if self.height == 0 else len(self.rows[0])

    def get_val_at(self, x: int, y: int) -> str:
        return self.rows[y][x]

    def is_on_grid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def foreach(self, func):
        for x in range(self.width):
            for y in range(self.height):
                func(x, y)

    def convert_to_int_vals(self):
        def convert_field_to_int(x: int, y: int) -> None:
            self.rows[y][x] = int(self.get_val_at(x, y))

        self.foreach(convert_field_to_int)
