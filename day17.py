from time import time

from util.args import parse_args
from util.submit import submit_answer


class AdvInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        a_val = self.hw.registers['A']
        denominator = 2 ** self.hw.get_next_combo_operant()
        self.hw.registers['A'] = a_val // denominator


class BxlInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        b_val = self.hw.registers['B']
        self.hw.registers['B'] = b_val ^ self.hw.get_next_literal_operant()


class BstInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        self.hw.registers['B'] = self.hw.get_next_combo_operant() % 8


class JnzInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        if self.hw.registers['A'] != 0:
            self.hw.registers['IP'] = self.hw.get_next_literal_operant() - 2


class BxcInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        self.hw.registers['B'] = self.hw.registers['C'] ^ self.hw.registers['B']


class OutInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        val = self.hw.get_next_combo_operant() % 8
        self.hw.output.append(val)


class BdvInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        a_val = self.hw.registers['A']
        denominator = 2 ** self.hw.get_next_combo_operant()
        self.hw.registers['B'] = a_val // denominator


class CdvInstruction:
    def __init__(self, hw):
        self.hw = hw

    def execute(self):
        a_val = self.hw.registers['A']
        denominator = 2 ** self.hw.get_next_combo_operant()
        self.hw.registers['C'] = a_val // denominator


INSTRUCTIONS = {
    0: AdvInstruction,
    1: BxlInstruction,
    2: BstInstruction,
    3: JnzInstruction,
    4: BxcInstruction,
    5: OutInstruction,
    6: BdvInstruction,
    7: CdvInstruction,
}


class Hardware:
    def __init__(self, registers, memory):
        self.registers = registers
        self.memory = memory

        self.output = []

    def get_next_combo_operant(self):
        val = self.memory[self.registers['IP'] + 1]
        if 0 <= val <= 3:
            return val

        match val:
            case 4:
                return self.registers['A']
            case 5:
                return self.registers['B']
            case 6:
                return self.registers['C']

        raise ValueError(f'Invalid operand {val}')

    def get_next_literal_operant(self):
        return self.memory[self.registers['IP'] + 1]

    def execute_next(self):
        op_code = self.memory[self.registers['IP']]

        next_instruction = INSTRUCTIONS[op_code](self)

        next_instruction.execute()

        self.registers['IP'] += 2

    def is_terminated(self):
        return self.registers['IP'] >= len(self.memory)


if __name__ == '__main__':
    args = parse_args()

    with args.puzzle_input as file:
        a_reg = int(file.readline().split(' ')[2])
        b_reg = int(file.readline().split(' ')[2])
        c_reg = int(file.readline().split(' ')[2])
        file.readline()
        prog = file.readline().split(' ')[1]
        prog = [int(val) for val in prog.split(',')]

    start = round(time() * 1000)

    registers = {
        'A': a_reg,
        'B': b_reg,
        'C': c_reg,
        'IP': 0
    }

    hw = Hardware(registers, prog)

    while not hw.is_terminated():
        hw.execute_next()

    answer_1 = ','.join([str(val) for val in hw.output])

    end_1 = round(time() * 1000)

    idx = len(prog) - 1

    octal_digits = [0] * len(prog)
    octal_digits[-1] = 1

    while idx >= 0:
        a_reg = 0
        for i in range(len(octal_digits)):
            a_reg += 8 ** i * octal_digits[i]

        registers = {
            'A': a_reg,
            'B': b_reg,
            'C': c_reg,
            'IP': 0
        }

        hw = Hardware(registers, prog)

        while not hw.is_terminated():
            hw.execute_next()

        if hw.output[idx] != prog[idx]:
            octal_digits[idx] += 1

            if octal_digits[idx] == 8:
                octal_digits[idx] = 0
                idx += 1
                octal_digits[idx] += 1
        else:
            idx -= 1

    answer_2 = a_reg

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 17, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 17, 2))
