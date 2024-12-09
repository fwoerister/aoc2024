from time import time

from util.args import parse_args
from util.submit import submit_answer


def calculate_checksum(diskmap: str):
    if len(diskmap) % 2 == 0:
        diskmap = diskmap[:-1]
    diskmap = [int(b) for b in list(diskmap)]

    disk = []
    b_id = 0

    idx = 0
    while idx < len(diskmap):
        if idx % 2 == 0:
            disk.extend([b_id] * diskmap[idx])
            b_id += 1
        else:
            disk.extend([-1] * diskmap[idx])
        idx += 1

    free_idx = disk.index(-1)
    data_idx = len(disk) - 1

    while disk.count(-1) > 0 and free_idx < data_idx:
        if disk[data_idx] == -1:
            data_idx -= 1
        else:
            disk[free_idx] = disk[data_idx]
            disk[data_idx] = -1

            free_idx = disk.index(-1)
            data_idx -= 1

    idx = 0
    checksum = 0
    while idx < len(disk):
        if disk[idx] != -1:
            checksum += idx * disk[idx]
        idx += 1

    return checksum


def calculate_checksum2(diskmap: str):
    if len(diskmap) % 2 == 0:
        diskmap = diskmap[:-1]
    diskmap = [int(b) for b in list(diskmap)]
    disk = []

    idx = 0
    while idx < len(diskmap):
        if idx % 2 == 0:
            disk.append([[idx // 2] * diskmap[idx]])
        else:
            disk.append([])

    for data_block in range(len(diskmap) - 1, 0, -2):
        for free_block in range(1, len(diskmap), 2):
            if len(disk[data_block]) <= len(disk[free_block]):
                disk[free_block].extend(disk[data_block])
                disk[data_block] = []


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        disk_map = file.readlines()[0].strip()
        start = round(time() * 1000)

        answer_1 = calculate_checksum(disk_map)

        end_1 = round(time() * 1000)

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 9, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 9, 2))
