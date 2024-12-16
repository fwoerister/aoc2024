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


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        if self.x > other.x:
            return True
        if self.x == other.x and self.y > other.y:
            return True

        return False

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))


class DirectionVector(Vector2D):
    def __init__(self, x, y):
        super().__init__(x, y)

    @staticmethod
    def from_char(direction_char):
        match direction_char:
            case '^':
                return DirectionVector(0, -1)
            case 'v':
                return DirectionVector(0, 1)
            case '<':
                return DirectionVector(-1, 0)
            case '>':
                return DirectionVector(1, 0)

    def rotate_clockwise(self):
        return DirectionVector(-self.y, self.x)

    def rotate_counter_clockwise(self):
        return DirectionVector(self.y, -self.x)

    def to_char(self):
        match (self.x, self.y):
            case (1, 0):
                return '>'
            case (-1, 0):
                return '<'
            case (0, 1):
                return 'v'
            case (0, -1):
                return '^'
