class Node:
  def __init__(self, no_of_children, metadata_entries):
    self.children_count = no_of_children
    self.metadata_count = metadata_entries
    self.children = []
    self.metadata = []
    self.value = 0

  def __repr__(self):
    return 'C: {0} M: {1}'.format(self.children_count, self.metadata_count)

def build_tree(head_node, numbers, numbers_index):
  # First, fill in the children
  while len(head_node.children) != head_node.children_count:
    child_node = Node(numbers[numbers_index], numbers[numbers_index+1])
    numbers_index += 2
    new_node, numbers_index = build_tree(child_node, numbers, numbers_index)
    head_node.children.append(new_node)

  # Now, fill in the metadata
  while len(head_node.metadata) != head_node.metadata_count:
    head_node.metadata.append(numbers[numbers_index])
    numbers_index += 1

  return head_node, numbers_index

def get_total_metadata(head_node):
  total = 0
  for m in head_node.metadata:
    total += m
  for c in head_node.children:
      total += get_total_metadata(c)
  return total

def calculate_value(head_node):
  if not head_node.children_count:
    value = sum(head_node.metadata)
    head_node.value = value
    return

  value = 0
  for child_index in head_node.metadata:
    if child_index > len(head_node.children):
      continue
    child_node = head_node.children[child_index-1]
    if not child_node.value:
      calculate_value(child_node)
    value += child_node.value
  head_node.value = value

def main():
  # 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
  numbers = list(map(int, open('input.txt', 'r').readline().split()))
  
  head_node = Node(numbers[0], numbers[1])
  numbers_index = 2
  build_tree(head_node, numbers, numbers_index)

  # Part 1
  sum_metadata_entries = get_total_metadata(head_node)
  print(sum_metadata_entries)

  # Part 2
  calculate_value(head_node)
  print(head_node.value)

if __name__ == '__main__':
  main()
