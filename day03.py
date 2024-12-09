import re

from util.args import parse_args

if __name__ == '__main__':
    args = parse_args()
    add_mul_to_result = True
    result = 0

    with args.puzzle_input as file:
        memory = ''.join(file.readlines())

        for group in re.findall(r"mul\((\d+,\d+)\)|(do\(\))|(don't\(\))", memory):
            if group[0] != "" and add_mul_to_result:
                left = int(group[0].split(',')[0])
                right = int(group[0].split(',')[1])
                result += left * right
            elif group[1] == "do()":
                add_mul_to_result = True
            elif group[2] == "don't()":
                add_mul_to_result = False

    print(result)
