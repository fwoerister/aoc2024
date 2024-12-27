import re
from time import time

from util.args import parse_args
from util.submit import submit_answer

GATE_FUNCTIONS = {
    'AND': lambda a, b: a & b,
    'OR': lambda a, b: a | b,
    'XOR': lambda a, b: a ^ b,
}


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


def init_wires(pos, x, y, carry_in):
    digits_x = [0] * 45
    digits_y = [0] * 45

    if x:
        digits_x[pos] = 1
    if y:
        digits_y[pos] = 1

    if pos > 0 and carry_in:
        digits_x[pos - 1] = 1
        digits_y[pos - 1] = 1

    wires = {}

    for idx in range(0, len(digits_x)):
        idx_str = str(idx).rjust(2, '0')
        wires[f'x{idx_str}'] = digits_x[idx]

    for idx in range(0, len(digits_y)):
        idx_str = str(idx).rjust(2, '0')
        wires[f'y{idx_str}'] = digits_y[idx]

    return wires


def process_gates(gates, wires):
    while gates:
        op1, operator, op2, result_wire = gates[0]

        if op1 in wires and op2 in wires:
            result_value = GATE_FUNCTIONS[operator](wires[op1], wires[op2])
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


def rename_gate(old, new, gates, only_output=False):
    new_gates = []
    for gate in gates:
        op1, operator, op2, result_wire = gate

        if not only_output:
            if op1 == old:
                op1 = new
            if op2 == old:
                op2 = new
        if result_wire == old:
            result_wire = new

        new_gates.append((op1, operator, op2, result_wire))
    return new_gates


def swap_gates(old, new, gates):
    gates = rename_gate(old, new + '_', gates, only_output=True)
    gates = rename_gate(new, old, gates, only_output=True)
    return rename_gate(new + '_', new, gates)


def find_gate(gates, operator, op1=None, op2=None):
    found_gates = []
    for g in [g for g in gates if g[1] == operator]:
        g_op1, g_operator, g_op2, g_output = g

        if op1 and op2:
            if (g_op1 == op1 and g_op2 == op2) or (g_op1 == op2 and g_op2 == op1):
                found_gates.append(g_output)
        else:
            if op1 and op1 in [g_op1, g_op2]:
                found_gates.append(g_output)
            if op2 and op2 in [g_op1, g_op2]:
                found_gates.append(g_output)

    return found_gates


def find_potential_operand(gates, operator, op):
    potential_operands = []
    for g in gates:
        g_op1, g_operator, g_op2, g_output = g

        if operator == g_operator:
            if op == g_op1:
                potential_operands.append(g_op2)
            if op == g_op2:
                potential_operands.append(g_op1)
    return potential_operands


def fix_adder(gates, pos, swaps):
    if pos == 0:
        z00 = find_gate(gates, 'XOR', op1='x00', op2='y00')
        c00 = find_gate(gates, 'AND', op1='x00', op2='y00')
        gates = rename_gate(z00[0], 'z00', gates)
        gates = rename_gate(c00[0], 'c00', gates)

        return fix_adder(gates, pos + 1, swaps)
    elif len(swaps) > 4:
        return None
    elif pos == 45:
        return swaps
    else:
        idx_str = str(pos).rjust(2, '0')
        c_in = f'c{str(pos - 1).rjust(2, '0')}'

        zp = find_gate(gates, 'XOR', f'x{idx_str}', f'y{idx_str}')
        z = find_gate(gates, 'XOR', zp[0], c_in)

        if not z:
            for potential_operand in find_potential_operand(gates, 'XOR', zp[0]):
                new_swaps = swaps + [(potential_operand, c_in)]
                new_gates = swap_gates(potential_operand, c_in, gates)

                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps

            for potential_operand in find_potential_operand(gates, 'XOR', c_in):
                new_swaps = swaps + [(potential_operand, zp[0])]
                new_gates = swap_gates(potential_operand, zp[0], gates)

                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps
            return None
        elif z[0] != f'z{idx_str}':
            new_swaps = swaps + [(z[0], f'z{idx_str}')]
            new_gates = swap_gates(z[0], f'z{idx_str}', gates)
            return fix_adder(new_gates, pos, new_swaps)

        c1 = find_gate(gates, 'AND', f'x{idx_str}', f'y{idx_str}')

        if not c1:
            return None

        c2 = find_gate(gates, 'AND', zp[0], c_in)

        if not c2:

            for potential_operand in find_potential_operand(gates, 'AND', zp[0]):
                new_swaps = swaps + [(potential_operand, zp[0])]
                new_gates = swap_gates(potential_operand, zp[0], gates)
                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps

            for potential_operand in find_potential_operand(gates, 'AND', c_in):
                new_swaps = swaps + [(potential_operand, c_in)]
                new_gates = swap_gates(potential_operand, c_in)
                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps

            return None

        c = find_gate(gates, 'OR', c1[0], c2[0])

        if not c:
            for potential_operand in find_potential_operand(gates, 'OR', c1[0]):
                new_swaps = swaps + [(potential_operand, c2[0])]
                new_gates = swap_gates(potential_operand, c2[0], gates)
                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps

            for potential_operand in find_potential_operand(gates, 'OR', c2[0]):
                new_swaps = swaps + [(potential_operand, c1[0])]
                new_gates = swap_gates(potential_operand, c1[0], gates)
                if final_swaps := fix_adder(new_gates, pos, new_swaps):
                    return final_swaps
            return None

        gates = rename_gate(zp[0], f'zp{idx_str}', gates)
        gates = rename_gate(z[0], f'z{idx_str}', gates)
        gates = rename_gate(c1[0], f'c1_{idx_str}', gates)
        gates = rename_gate(c2[0], f'c2_{idx_str}', gates)
        gates = rename_gate(c[0], f'c{idx_str}', gates)

        return fix_adder(gates, pos + 1, swaps)


if '__main__' == __name__:
    args = parse_args()

    wires, gates = parse_input(args.puzzle_input)

    start = round(time() * 1000)

    answer_1 = int(process_gates(gates, wires), 2)

    end_1 = round(time() * 1000)

    answer_2 = 0

    involved_gates = set()
    for swap in fix_adder(gates, 0, []):
        involved_gates.add(swap[0])
        involved_gates.add(swap[1])

    gate_list = list(involved_gates)
    gate_list.sort()

    answer_2 = ','.join(gate_list)

    end_2 = round(time() * 1000)

    print(answer_1)
    print(f'time: {end_1 - start}ms')

    print(answer_2)
    print(f'time: {end_2 - end_1}ms')

    if args.submit == 1:
        print(submit_answer(answer_1, 24, 1))

    if args.submit == 2:
        print(submit_answer(answer_2, 24, 2))
