import re
from time import time

from util.args import parse_args
from util.submit import submit_answer


def find_output_for(gate, gates):
    for g in gates:
        op1, operation, op2, output = g

        if (op1, operation, op2) == gate:
            return output

        if (op2, operation, op1) == gate:
            return output


def swap_gates(old, new, gates):
    gates = rename_gate(old, new + '_', gates)
    gates = rename_gate(new, old, gates)
    return rename_gate(new + '_', new, gates)


def set_wire_to(wires, prefix, digits):
    for idx in range(0, len(digits)):
        idx_str = str(idx).rjust(2, '0')
        wires[f'{prefix}{idx_str}'] = digits[idx]
    return wires


def test_digit(gates, position):
    digits_x = [0] * 45
    digits_y = [0] * 45

    wires = {}
    set_wire_to(wires, 'x', digits_x)
    set_wire_to(wires, 'y', digits_y)

    result = process_gates(gates, wires)

    result = list(result)
    result.reverse()

    if result[position] != '0' and result[position + 1] != '0':
        return False

    digits_x = [0] * 45
    digits_y = [0] * 45

    digits_x[position] = 1

    wires = {}
    set_wire_to(wires, 'x', digits_x)
    set_wire_to(wires, 'y', digits_y)

    result = process_gates(gates, wires)

    result = list(result)
    result.reverse()

    if result[position] != '1' and result[position + 1] != '0':
        return False

    digits_x = [0] * 45
    digits_y = [0] * 45

    digits_y[position] = 1

    wires = {}
    set_wire_to(wires, 'x', digits_x)
    set_wire_to(wires, 'y', digits_y)

    result = process_gates(gates, wires)

    result = list(result)
    result.reverse()

    if result[position] != '1' and result[position + 1] != '0':
        return False

    digits_x = [0] * 45
    digits_y = [0] * 45

    digits_x[position] = 1
    digits_y[position] = 1

    wires = {}
    set_wire_to(wires, 'x', digits_x)
    set_wire_to(wires, 'y', digits_y)

    result = process_gates(gates, wires)

    result = list(result)
    result.reverse()

    if result[position] != '0' and result[position + 1] != '1':
        return False

    if position > 0:
        digits_x = [0] * 45
        digits_y = [0] * 45

        digits_x[position - 1] = 1
        digits_y[position - 1] = 1
        digits_x[position] = 1

        wires = {}
        set_wire_to(wires, 'x', digits_x)
        set_wire_to(wires, 'y', digits_y)

        result = process_gates(gates, wires)

        result = list(result)
        result.reverse()

        if result[position - 1] != '0' and result[position] != '0' and result[position + 1] != '1':
            return False

        digits_x = [0] * 45
        digits_y = [0] * 45

        digits_x[position - 1] = 1
        digits_y[position - 1] = 1
        digits_y[position] = 1

        wires = {}
        set_wire_to(wires, 'x', digits_x)
        set_wire_to(wires, 'y', digits_y)

        result = process_gates(gates, wires)

        result = list(result)
        result.reverse()

        if result[position - 1] != '0' and result[position] != '0' and result[position + 1] != '1':
            return False

        digits_x = [0] * 45
        digits_y = [0] * 45

        digits_x[position - 1] = 1
        digits_y[position - 1] = 1
        digits_x[position] = 1
        digits_y[position] = 1

        wires = {}
        set_wire_to(wires, 'x', digits_x)
        set_wire_to(wires, 'y', digits_y)

        result = process_gates(gates, wires)

        result = list(result)
        result.reverse()

        if result[position - 1] != '0' and result[position] != '1' and result[position + 1] != '1':
            return False

    return True


def parse_input(puzzle_input):
    with puzzle_input as f:
        wires = {}
        while (line := f.readline()) != '\n':
            name, value = line.split(': ')
            value = int(value)
            wires[name] = value

        gates = []
        while line := f.readline():
            result = re.search(r'(.{3}) (AND|XOR|OR) (.{3}) -> (.{3})', line)

            gates.append(result.groups())

        return wires, gates


PROCESS_GATE = {
    'AND': lambda a, b: a & b,
    'OR': lambda a, b: a | b,
    'XOR': lambda a, b: a ^ b,
}


def process_gates(gates, wires):
    while gates:
        op1, operator, op2, result_wire = gates[0]

        if op1 in wires and op2 in wires:
            result_value = PROCESS_GATE[operator](wires[op1], wires[op2])
            wires[result_wire] = result_value
            gates = gates[1:]
        else:
            gates = gates[1:] + [gates[0]]

    return extract_number('z', wires)


def extract_number(prefix, wires):
    digits = []

    for wire in wires:
        if wire.startswith(prefix):
            digits.append((wire, wires[wire]))

    digits.sort(reverse=True)
    return ''.join([str(wire[1]) for wire in digits])


def find_gate_by_output(wire, gates):
    for gate in gates:
        if gate[3] == wire:
            return gate
    return None


def extract_gates(starting_wire, gates):
    found_gates = {starting_wire}
    size_of_gates = -1

    while size_of_gates < len(found_gates):
        size_of_gates = len(found_gates)

        new_gates = set()

        for output_wire in found_gates:
            current_gate = find_gate_by_output(output_wire, gates)
            if current_gate:
                if left_parent := find_gate_by_output(current_gate[0], gates):
                    new_gates.add(left_parent[3])
                if right_parent := find_gate_by_output(current_gate[2], gates):
                    new_gates.add(right_parent[3])
        found_gates = found_gates.union(new_gates)
    return found_gates


def rename_gate(old, new, gates):
    new_gates = []
    for gate in gates:
        op1, operator, op2, result_wire = gate

        if op1 == old:
            op1 = new
        if op2 == old:
            op2 = new
        if result_wire == old:
            result_wire = new

        new_gates.append((op1, operator, op2, result_wire))
    return new_gates


if '__main__' == __name__:
    args = parse_args()

    wires, gates = parse_input(args.puzzle_input)

    start = round(time() * 1000)

    answer_1 = process_gates(gates, wires)

    end_1 = round(time() * 1000)

    answer_2 = 0

    for idx in range(1, 45):
        idx_str = str(idx).rjust(2, '0')
        if not test_digit(gates, idx):
            if idx == 0:
                z = find_output_for((f'x{idx_str}', 'XOR', f'y{idx_str}'), gates)
                c_out = find_output_for((f'x{idx_str}', 'AND', f'y{idx_str}'), gates)
                gates = rename_gate(c_out, f'z00', gates)
                gates = rename_gate(c_out, f'c00', gates)
            else:
                zp = find_output_for((f'x{idx_str}', 'XOR', f'y{idx_str}'), gates)
                c_in = f'c{str(idx - 1).rjust(2, '0')}'
                z = find_output_for((op1= ), gates)

                c_out1 = find_output_for((zp, 'AND', c_in), gates)
                c_out2 = find_output_for((f'x{idx_str}', 'AND', f'y{idx_str}'), gates)

                c_out = find_output_for((c_out1, 'OR', c_out2), gates)

                gates = rename_gate('zp', f'zp{idx_str}', gates)
                gates = rename_gate(c_out, f'c{idx_str}', gates)
        else:
            print('error')

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 24, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 24, 2))
