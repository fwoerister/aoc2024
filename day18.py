from heapq import heappush, heappop
from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer

SIZE = 71
BYTES_FALLEN = 1024


class Memory(Grid):
    def __init__(self, width, height, byte_pos):
        rows = ['.' * width] * height
        super().__init__(rows)

        self.start = (0, 0)
        self.end = (width - 1, height - 1)
        self.byte_pos = byte_pos

    def find_shortest_path_after(self, num_bytes):
        byte_pos = set(self.byte_pos[:num_bytes])

        open_pos = []
        heappush(open_pos, (0, self.start, [self.start]))
        visited = {self.start}

        while open_pos:
            path_length, current, path = heappop(open_pos)

            if current == self.end:
                return path_length, path

            neighbours = filter(lambda nb: nb not in byte_pos, self.get_neighbours(*current))

            for n in neighbours:
                if n not in visited:
                    visited.add(n)
                    heappush(open_pos, (path_length + 1, n, path + [n]))

        return -1, None


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        byte_pos = []

        for line in file:
            x, y = line.strip().split(',')
            byte_pos.append((int(x), int(y)))

        start = round(time() * 1000)

        mem = Memory(SIZE, SIZE, byte_pos)
        answer_1, _ = mem.find_shortest_path_after(BYTES_FALLEN)

    end_1 = round(time() * 1000)

    mem = Memory(SIZE, SIZE, byte_pos)

    idx = 0
    while idx < len(byte_pos) + 1:
        path_length, path = mem.find_shortest_path_after(idx)

        if not path:
            answer_2 = byte_pos[idx - 1]
            break

        while byte_pos[idx - 1] not in path:
            idx += 1

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 18, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 18, 2))
