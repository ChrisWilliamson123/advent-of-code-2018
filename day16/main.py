import re
from collections import defaultdict
from functions import *

def parse_instructions(input_lines):
  instructions = defaultdict(int)
  index = 0
  while len(input_lines[index]) > 0 and input_lines[index][0] == 'B':
    instructions[len(instructions)+1] = {
      'before': [int(x) for x in re.findall(r'\d+', input_lines[index])],
      'instruction': [int(x) for x in re.findall(r'\d+', input_lines[index+1])],
      'after': [int(x) for x in re.findall(r'\d+', input_lines[index+2])]
    }
    index += 4
  return instructions

def reduce_opcodes(opcodes):
    single_instruction_opcodes = {o: i for o, i in opcodes.items() if len(i) == 1}
    while len(single_instruction_opcodes) != len(opcodes):
        for o_1, i_1 in single_instruction_opcodes.items():
            for o_2, i_2 in opcodes.items():
                if o_2 != o_1 and i_1[0] in i_2:
                    i_2.pop(i_2.index(i_1[0]))
        single_instruction_opcodes = {o: i for o, i in opcodes.items() if len(i) == 1}
    return opcodes
    


def main():
    whole_input = [l.rstrip() for l in open('input.txt', 'r').readlines()]
    samples = parse_instructions(whole_input)
    opcodes = defaultdict(list)

    more_than_three = 0
    for data in samples.values():
        before_state = data['before']
        i = data['instruction']
        after_state = data['after']
        opcode = i[0]

        results = {f.__name__: f(before_state, i[1], i[2], i[3]) for f in all_instruction_functions}
        correct_instructions = [i_name for i_name, r in results.items() if r == after_state]

        opcodes[opcode] = correct_instructions

        if len(correct_instructions) >= 3:
            more_than_three += 1

    print('Part 1: {0}'.format(more_than_three))

    opcodes = reduce_opcodes(opcodes)

    test_program_instructions = [x.rstrip() for x in open('test_program.txt', 'r').readlines()]
    test_program_instructions = [[int(y) for y in re.findall('\d+', x)] for x in test_program_instructions]
    registers = [0, 0, 0, 0]

    for idx, i in enumerate(test_program_instructions):
        opcode = i[0]
        to_execute = opcodes[opcode][0]
        result = eval('{0}({1}, {2}, {3}, {4})'.format(to_execute, registers, i[1], i[2], i[3]))
        registers = result
    
    print('Part 2: {0}'.format(registers[0]))

if __name__ == '__main__':
    main()