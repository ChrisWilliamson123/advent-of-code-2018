from collections import defaultdict
from functions import *

def parse_input(input_lines):
    ip = int(input_lines[0].split()[1])
    instructions = defaultdict(dict)
    for idx, i in enumerate(input_lines[1:]):
        i_split = i.split()
        instructions[idx] = {
            'operation': i_split[0],
            'A': int(i_split[1]),
            'B': int(i_split[2]),
            'output_reg': int(i_split[3])
        }
    return ip, instructions

def main():
    instruction_pointer_register, instructions = parse_input([l.rstrip() for l in open('input.txt', 'r').readlines()])
    # registers = [1, 0, 10551287, 3, 3, 10551287]
    # registers = [128, 0, 10551287, 127, 3, 10551287]
    registers = [10708661, 0, 10551287, 10551287, 3, 10551287]
    instruction_pointer_value = 3

    # while registers[3] < registers[2]:
    #     if registers[3] % 1000000 == 0:
    #         print(registers)
    #     if registers[2] % registers[3] != 0 or (registers[2] % registers[3] == 0 and registers[0] > registers[3]):
    #         registers[5] = registers[2]
    #     elif registers[0] < registers[3]:
    #         registers[5] = int(registers[2] / registers[3])
    #     # else:
    #     #     registers[5] = registers[2]

    #     # state before: r1 will be r3 * r5-1

    #     registers[1] = registers[3] * registers[5]
    #     if registers[1] == registers[2]:
    #         registers[1] = 1
    #         # inst 7
    #         registers[0] = registers[3] + registers[0]
    #     else:
    #         registers[1] = 0
    #     registers[5] += 1
    #     if registers[5] > registers[2]:
    #         registers[1] = 1
    #         registers[3] += 1
    #         registers[5] = 1
    #     else:
    #         registers[1] = 0
    #     # print(registers, end="\r")
    #     # print(registers)
    # print(registers)


    while -1 < instruction_pointer_value < len(instructions):
        current_instruction = instructions[instruction_pointer_value]
        # print(current_instruction)
        old_registers = registers
        registers[instruction_pointer_register] = instruction_pointer_value
        new_registers = eval('{0}({1}, {2}, {3}, {4})'.format(
            current_instruction['operation'],
            registers,
            current_instruction['A'],
            current_instruction['B'],
            current_instruction['output_reg'])
        )
        new_instruction_pointer_value = new_registers[instruction_pointer_register] + 1
        print('ip={0} {1} {2} {3} {4} {5} {6}'.format(
            instruction_pointer_value,
            old_registers
            ,
            current_instruction['operation'],
            current_instruction['A'],
            current_instruction['B'],
            current_instruction['output_reg'],
            new_registers
        ))
        registers = new_registers
        instruction_pointer_value = new_instruction_pointer_value
        # print(instruction_pointer_value)
        # print(registers)
        
    print(registers)


# def inner_loop():
#     while r1 < r2:
#         r4 = r1 + r4
#         r0 = r3 + r0
#         r5 = r5 + 1
#         if r5 > r2:
#             r1 = 1
#         else:
#             r1 = 0
#         r4 = r4 + r1




if __name__ == '__main__':
    main()
