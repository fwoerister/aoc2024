from itertools import product
from time import time

from util.args import parse_args
from util.datastructures import Grid
from util.submit import submit_answer


class AntennaGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows)

        self.antennas = {}

        def add_antenna_to_dict(x, y):
            if (antenna_id := self.get_val_at(x, y)) != '.':
                if antenna_id not in self.antennas:
                    self.antennas[antenna_id] = [(x, y)]
                else:
                    self.antennas[antenna_id].append((x, y))

        self.foreach(add_antenna_to_dict)

    def get_antinodes(self, antenna_id, include_resonate_harmonic=False):
        anti_nodes = set()
        for antenna_1, antenna_2 in product(self.antennas[antenna_id], self.antennas[antenna_id]):
            if antenna_1 != antenna_2:
                diff = (antenna_2[0] - antenna_1[0], antenna_2[1] - antenna_1[1])
                anti_node = (antenna_2[0] + diff[0], antenna_2[1] + diff[1])

                if include_resonate_harmonic:
                    anti_node = antenna_2
                    while self.is_on_grid(*anti_node):
                        anti_nodes.add(anti_node)
                        anti_node = (anti_node[0] + diff[0], anti_node[1] + diff[1])
                else:
                    if self.is_on_grid(*anti_node):
                        anti_nodes.add(anti_node)

        return anti_nodes

    def get_all_anti_nodes(self, include_resonate_harmonic=False):
        anti_nodes = set()

        for antenna_id in self.antennas:
            anti_nodes.update(self.get_antinodes(antenna_id, include_resonate_harmonic))

        return anti_nodes


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:

        antenna_map = AntennaGrid(file.readlines())

        start = round(time() * 1000)
        answer_1 = len(antenna_map.get_all_anti_nodes(False))

        end_1 = round(time() * 1000)

        answer_2 = len(antenna_map.get_all_anti_nodes(True))

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 8, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 8, 2))
