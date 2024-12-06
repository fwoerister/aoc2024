from util.args import parse_args
from util.submit import submit_answer


def parse_successor_rules(input_file):
    line = input_file.readline()
    rules = {}

    while line != "\n":
        left, right = line.strip().split('|')

        if left in rules:
            rules[left].append(right)
        else:
            rules[left] = [right]

        line = input_file.readline()

    return rules


def parse_update_pages(input_file):
    pages = []
    while line := input_file.readline():
        pages.append(line.strip().split(','))
    return pages


def check_if_valid(update, successor_of):
    for page in update:
        if page in successor_of:
            for succeeding_page in successor_of[page]:
                if succeeding_page in update and update.index(succeeding_page) < update.index(page):
                    return False
    return True


def fix_first_pos(update, successor_of):
    first = update[0]

    # find last conflicting position
    new_idx = -1
    for remaining_page in update[1:]:
        if remaining_page in successor_of and first in successor_of[remaining_page]:
            new_idx = update.index(remaining_page)

    # if there is a conflict, move first page behind the last conflicting page
    if new_idx != -1:
        return update[1:new_idx + 1] + [first] + update[new_idx + 1:]

    return update


def fix_update(update, successor_of):
    if len(update) == 1:
        return update

    head = update[0]

    update = fix_first_pos(update, successor_of)

    if head == update[0]:
        return [head] + fix_update(update[1:], successor_of)

    return fix_update(update, successor_of)


if __name__ == '__main__':
    args = parse_args()
    answer_1 = 0
    answer_2 = 0

    with args.puzzle_input as file:
        successors_of_rules = parse_successor_rules(file)
        manual_pages = parse_update_pages(file)

    for manual_update in manual_pages:
        if check_if_valid(manual_update, successors_of_rules):
            answer_1 += int(manual_update[len(manual_update) // 2])
        else:
            new_update = fix_update(manual_update, successors_of_rules)
            answer_2 += int(new_update[len(new_update) // 2])

    print(answer_1)
    print(answer_2)

    if args.submit == 1:
        print(submit_answer(answer_1, 5, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 5, 2))
