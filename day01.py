from util.args import parse_args

if __name__ == '__main__':
    left_list = []
    right_list = []

    args = parse_args()

    with args.puzzle_input as file:
        for line in file.readlines():
            left_val, right_val = line.split('   ')
            left_list.append(int(left_val))
            right_list.append(int(right_val))

    left_list.sort()
    right_list.sort()

    distances = list(map(lambda id_tuple: abs(id_tuple[0] - id_tuple[1]), zip(left_list, right_list)))

    print(f"total distance: {sum(distances)}")

    sim_score = 0

    for val in left_list:
        sim_score += val * right_list.count(val)

    print(f"similarity score: {sim_score}")