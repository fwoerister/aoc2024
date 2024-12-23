from time import time

from util.args import parse_args


def calculate_next_secret(secret):
    secret = (secret ^ (secret * 64)) % 16777216
    secret = (secret ^ (secret // 32)) % 16777216
    secret = (secret ^ (secret * 2048)) % 16777216

    return secret


if '__main__' == __name__:
    args = parse_args()

    with args.puzzle_input as file:
        initial_secrets = [int(val.strip()) for val in file.readlines() if val]

    start = round(time() * 1000)

    answer_1 = 0
    for secret in initial_secrets:
        for i in range(2000):
            secret = calculate_next_secret(secret)
        answer_1 += secret

    end_1 = round(time() * 1000)

    sellers = []
    for secret in initial_secrets:
        prices = [secret % 10]
        diffs = [None]

        for i in range(2000):
            secret = calculate_next_secret(secret)
            prices.append(secret % 10)
            diffs.append(prices[-1] - prices[-2])
        sellers.append({'prices': prices, 'diffs': diffs})

    answer_2 = 0
    sums = {}

    for seller in sellers:
        visited = set()
        for idx in range(1, len(seller['prices']) - 3):
            seq = tuple(seller['diffs'][idx:idx + 4])

            if seq not in visited:
                if seq not in sums:
                    sums[seq] = seller['prices'][idx + 3]
                else:
                    sums[seq] += seller['prices'][idx + 3]

            visited.add(seq)

    answer_2 = max(sums.values())

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 22, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 22, 2))
