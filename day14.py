import re
from time import time

from util.args import parse_args
from util.submit import submit_answer

WIDTH = 101
HEIGHT = 103


def parse_robot_locations(lines):
    robots = []
    for line in lines:
        if line != '\n':
            px, py, vx, vy = [int(val) for val in re.findall(r'(\d*),(\d*) v=(-?\d*),(-?\d*)', line)[0]]

            robots.append({
                'px': px,
                'py': py,
                'vx': vx,
                'vy': vy,
            })

    return robots


def move_robot(robot, t):
    robot['px'] = (robot['px'] + robot['vx'] * t) % WIDTH
    robot['py'] = (robot['py'] + robot['vy'] * t) % HEIGHT


def get_quadrants(robots):
    h_mid = (WIDTH // 2)
    v_mid = (HEIGHT // 2)

    q1 = list(filter(lambda x: x['px'] < h_mid and x['py'] < v_mid, robots))
    q2 = list(filter(lambda x: x['px'] > h_mid and x['py'] < v_mid, robots))
    q3 = list(filter(lambda x: x['px'] < h_mid and x['py'] > v_mid, robots))
    q4 = list(filter(lambda x: x['px'] > h_mid and x['py'] > v_mid, robots))

    return q1, q2, q3, q4


def print_map(robots):
    for y in range(HEIGHT):
        line = ''
        for x in range(WIDTH):
            count = len(list(filter(lambda r: r['px'] == x and r['py'] == y, robots)))
            line += '.' if count == 0 else str(count)
        print(line + '\n')


def could_be_x_mas_tree(robots):
    for r in robots:
        x = r['px']
        y = r['py']

        level1 = [
            len(list(filter(lambda r: r['px'] == x - 1 and r['py'] == y + 1, robots))),
            len(list(filter(lambda r: r['px'] == x + 1 and r['py'] == y + 1, robots))),
        ]

        if 0 in level1:
            continue

        level2 = [
            len(list(filter(lambda r: r['px'] == x - 2 and r['py'] == y + 2, robots))),
            len(list(filter(lambda r: r['px'] == x + 2 and r['py'] == y + 2, robots))),
        ]
        if 0 in level2:
            continue

        level3 = [
            len(list(filter(lambda r: r['px'] == x - 3 and r['py'] == y + 3, robots))),
            len(list(filter(lambda r: r['px'] == x + 3 and r['py'] == y + 3, robots))),
        ]

        if 0 not in level3:
            return True

    return False


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        lines = file.readlines()
        robots_l1 = parse_robot_locations(lines)
        robots_l2 = parse_robot_locations(lines)

    answer_1 = 0

    start = round(time() * 1000)

    for robot in robots_l1:
        move_robot(robot, 100)

    q1, q2, q3, q4 = get_quadrants(robots_l1)

    answer_1 = len(q1) * len(q2) * len(q3) * len(q4)

    end_1 = round(time() * 1000)

    answer_2 = 0

    while not could_be_x_mas_tree(robots_l2):
        answer_2 += 1
        for r in robots_l2:
            move_robot(r, 1)

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 11, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 11, 2))
