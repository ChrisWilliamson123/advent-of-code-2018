import re
from collections import defaultdict

class Instruction:

  def __init__(self, id):
    self.id = id
    self.complete = False
    self.next = []
    self.previous = []

  # def __str__(self):
  #   return 'Node {0}\n\tAfter: {1}\n\tBefore: {2}'.format(self.id, self.next, self.previous)

  def __repr__(self):
    return 'Node {0}'.format(self.id)

get_steps = lambda i: re.findall('step ([a-z])', i, re.IGNORECASE)

def parse_instructions(instructions):
  return list(map(get_steps, instructions))

def can_be_executed(instruction_node, completed_instructions):
  # print('Checking {0} {1} against {2}'.format(instruction_node, instruction_node.previous, completed_instructions))
  return set(instruction_node.previous) <= set(completed_instructions)

def build_instructions(instructions):
  ids_to_instructions = {}
  
  # First instruction
  before = instructions[0][0]
  after = instructions[0][1]
  head_node = Instruction(before)
  next_node = Instruction(after)
  head_node.next.append(next_node)
  next_node.previous.append(head_node)
  ids_to_instructions[before] = head_node
  ids_to_instructions[after] = next_node

  for i in instructions[1:]:
    before = i[0]
    after = i[1]

    before_node = ids_to_instructions[before] if before in ids_to_instructions else Instruction(before)
    after_node = ids_to_instructions[after] if after in ids_to_instructions else Instruction(after)

    before_node.next.append(after_node)
    before_node.next = sorted(before_node.next, key=lambda x: x.id)
    after_node.previous.append(before_node)
    after_node.previous = sorted(after_node.previous, key=lambda x: x.id)

    ids_to_instructions[before] = before_node
    ids_to_instructions[after] = after_node

    if after_node == head_node:
      head_node = before_node

  return (head_node, ids_to_instructions)

def get_possible_next_nodes(current_node):
  possible_nodes = []
  for node in current_node.next:
    if not list(filter(lambda x: x.complete == False, node.previous)) and not node.complete:
      possible_nodes.append(node)
  return possible_nodes

def backtrack(current_node):
  previous_completed_nodes = list(filter(lambda x: x.complete, current_node.previous))
  print('Previous completed nodes: {0}'.format(previous_completed_nodes))

  for n in previous_completed_nodes:
    print('Selected previous: {0}'.format(n))
    possible_next_nodes = get_possible_next_nodes(n)
    print('Possible next nodes: {0}'.format(possible_next_nodes))
    if possible_next_nodes:
      return possible_next_nodes[0]

  return backtrack(previous_completed_nodes[0])
  # selected_previous = previous_completed_nodes[0]



def main():
  instructions_text = [x.rstrip() for x in open('input.txt', 'r').readlines()]
  # [ [before, after] ]
  instructions = parse_instructions(instructions_text)

  head_node, ids_to_instructions = build_instructions(instructions)

  for id, i in sorted(ids_to_instructions.items(), key=lambda x: x[0]):
    print(id, i.next, i.previous)

  print('\nSTART NODE: {0}', head_node)

  completed_instructions = []
  while True:
    print('Current node: {0}'.format(head_node))
    
    head_node.complete = True
    completed_instructions.append(head_node)
    print(''.join([x.id for x in completed_instructions]))

    if len(completed_instructions) == len(ids_to_instructions):
      break
    # Get the list of possible next nodes
    possible_next_nodes = get_possible_next_nodes(head_node)
    print('Possible next nodes: {0}'.format(possible_next_nodes))

    if not possible_next_nodes:
      head_node = backtrack(head_node)
    else:
      head_node = possible_next_nodes[0]
    print('Next head: {0}'.format(head_node))
    # If there aren't any then go back to the closest node that has nexts to travel to
    # if not possilbe_next_nodes:
    #   next_node = backtrack(head_node)
    # else:
    #   head_node = possilbe_next_nodes[0]

  print(''.join([x.id for x in completed_instructions]))


if __name__ == '__main__':
  main()
