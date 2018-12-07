import re

class Instruction:

  def __init__(self, id):
    self.id = id
    self.complete = False
    self.next = []
    self.previous = []

  def __repr__(self):
    return 'Node {0}'.format(self.id)

get_steps = lambda i: re.findall('step ([a-z])', i, re.IGNORECASE)

def parse_instructions(instructions):
  return list(map(get_steps, instructions))

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

def get_next_available(current_node):
  potential_nexts = current_node.next
  actual_nexts = []

  for n in potential_nexts:
    incomplete_previous_nodes = list(filter(lambda x: x.complete == False, n.previous)) 
    if not incomplete_previous_nodes:
      actual_nexts.append(n)
  return actual_nexts

def build_times(nodes):
  times = {}
  for n in nodes:
    id = n.id
    times[n] = (ord(id)-64) + 60
  return(times)

def main():
  instructions_text = [x.rstrip() for x in open('input.txt', 'r').readlines()]
  instructions = parse_instructions(instructions_text)
  head_node, ids_to_instructions = build_instructions(instructions)

  instructions_to_times = build_times(ids_to_instructions.values())

  time_elapsed = 0
  in_progress = [head_node]
  all_available_nodes = []
  complete = []
  worker_limit = 5

  while len(in_progress) > 0:
    time_elapsed += 1
    for node in in_progress:
      instructions_to_times[node] -= 1
    for i, t in instructions_to_times.items():
      if t == 0 and i not in complete:
        complete.append(i)
        in_progress.remove(i)
        i.complete = True
        available = get_next_available(i)
        all_available_nodes += available
        all_available_nodes = sorted(all_available_nodes, key=lambda x: x.id)
        while len(in_progress) < worker_limit and len(all_available_nodes) > 0:
          in_progress.append(all_available_nodes[0])
          all_available_nodes.pop(0)
  print(time_elapsed)
    
if __name__ == '__main__':
  main()