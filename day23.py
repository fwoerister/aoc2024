from time import time

from util.args import parse_args


class ComputerNetwork:
    def __init__(self, connections):
        self.computers = dict()

        for con in connections:
            if con[0] not in self.computers:
                self.computers[con[0]] = [con[1]]
            else:
                self.computers[con[0]].append(con[1])

            if con[1] not in self.computers:
                self.computers[con[1]] = [con[0]]
            else:
                self.computers[con[1]].append(con[0])

    def count_groups(self, prefix):
        count = 0
        found = set()
        for c in [c for c in self.computers if c.startswith(prefix)]:
            for n1 in self.computers[c]:
                for n2 in self.computers[c]:
                    group = [c, n1, n2]
                    group.sort()
                    group = tuple(group)

                    if n1 != n2 and n1 in self.computers[n2] and group not in found:
                        found.add(group)
                        count += 1
        return count

    def find_password(self):
        max_cluster = []

        for seed in self.computers:
            cluster = [seed]
            for c in self.computers[seed]:
                if all([c in self.computers[member] for member in cluster]):
                    cluster.append(c)

            if len(cluster) > len(max_cluster):
                cluster.sort()
                max_cluster = cluster

        return ','.join(max_cluster)


if '__main__' == __name__:
    args = parse_args()

    with args.puzzle_input as file:
        connections = [line.strip().split('-') for line in file.readlines() if line]

    cn = ComputerNetwork(connections)

    answer_1 = 0
    start = round(time() * 1000)

    answer_1 = cn.count_groups('t')

    end_1 = round(time() * 1000)

    answer_2 = cn.find_password()

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 23, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 23, 2))
