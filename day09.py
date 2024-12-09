from functools import reduce
from time import time

from util.args import parse_args
from util.submit import submit_answer


def calculate_checksum(disk):
    checksum = 0
    for idx in range(len(disk)):
        if disk[idx] != -1:
            checksum += idx * disk[idx]
    return checksum


def diskmap_to_int(diskmap):
    if len(diskmap) % 2 == 0:
        diskmap = diskmap[:-1]
    return [int(b) for b in list(diskmap)]


def defrag_memory_level1(diskmap: str):
    diskmap = diskmap_to_int(diskmap)
    disk = [0] * diskmap[0]

    free_block_idx = 1
    data_block_idx = len(diskmap) - 1

    relocated_blocks = 0

    while free_block_idx < data_block_idx:

        free_block_size = diskmap[free_block_idx]
        data_block_size = diskmap[data_block_idx]

        if (relocated_blocks + data_block_size) < free_block_size:
            disk.extend([data_block_idx // 2] * data_block_size)
            relocated_blocks += data_block_size
            data_block_idx -= 2
        else:
            disk.extend([data_block_idx // 2] * (free_block_size - relocated_blocks))
            diskmap[data_block_idx] -= free_block_size - relocated_blocks
            relocated_blocks += free_block_size - relocated_blocks

            free_block_idx += 2
            relocated_blocks = 0

            disk.extend([free_block_idx // 2] * diskmap[free_block_idx - 1])

    return disk


def defrag_memory_level2(diskmap: str):
    diskmap = diskmap_to_int(diskmap)
    disk = []

    for idx in range(len(diskmap)):
        if idx % 2 == 0:
            disk.append([idx // 2] * diskmap[idx])
        else:
            disk.append([])

    for data_block_idx in range(len(diskmap) - 1, 0, -2):
        for free_block_idx in range(1, data_block_idx):
            free_block_size = diskmap[free_block_idx] - len(disk[free_block_idx])
            data_block_size = diskmap[data_block_idx]

            if data_block_size <= free_block_size:
                disk[free_block_idx].extend(disk[data_block_idx])
                disk[data_block_idx] = [-1] * diskmap[data_block_idx]
                break

    for free_block_idx in range(1, len(disk), 2):
        disk[free_block_idx].extend([-1] * (diskmap[free_block_idx] - len(disk[free_block_idx])))

    disk = reduce(lambda x, y: x + y, disk)

    return disk


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        disk_map = file.readlines()[0].strip()
        start = round(time() * 1000)

        disk_level1 = defrag_memory_level1(disk_map)
        answer_1 = calculate_checksum(disk_level1)

        end_1 = round(time() * 1000)

        disk_level2 = defrag_memory_level2(disk_map)
        answer_2 = calculate_checksum(disk_level2)

        end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')
    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 9, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 9, 2))
