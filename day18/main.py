import operator
from collections import defaultdict, Counter

ADJACENT_MODIFIERS = [
  (-1, -1),
  (0, -1),
  (1, -1),
  (-1, 0),
  (1, 0),
  (-1, 1),
  (0, 1),
  (1, 1)
]

def parse_input(input_lines):
  area = defaultdict(str)
  for y, l in enumerate(input_lines):
    for x, c in enumerate(l):
      area[(x, y)] = c
  return area, len(input_lines)-1

def get_adjacent_coords(origin, edge):
  adjacents = [tuple(map(operator.add, origin, m)) for m in ADJACENT_MODIFIERS]
  return [a for a in adjacents if 0 <= a[0] <= edge and 0 <= a[1] <= edge]

def get_contents_of_coords(coords, collection_area):
  values = [collection_area[co] for co in coords]
  return Counter(values)

def perform_transformations(collection_area, max_edge):
  new_collection_area = defaultdict(str)

  for coord, content in collection_area.items():
    adjacent_coords = get_adjacent_coords(coord, max_edge)
    content_counts = get_contents_of_coords(adjacent_coords, collection_area)

    if content == '.' and content_counts['|'] >= 3:
      new_collection_area[coord] = '|'
    elif content == '|' and content_counts['#'] >= 3:
      new_collection_area[coord] = '#'
    elif content == '#' and (content_counts['#'] < 1 or content_counts['|'] < 1):
      new_collection_area[coord] = '.'
    else:
      new_collection_area[coord] = content

  return new_collection_area

def main():
  collection_area, max_edge = parse_input([l.rstrip() for l in open('input.txt', 'r').readlines()])
  minutes = 10

  combinations_seen = defaultdict(list)
  results = defaultdict(int)
  result_found_via_pattern = False
  
  m = 1
  while m <= minutes and not result_found_via_pattern:
    collection_area = perform_transformations(collection_area, max_edge)
    counts = Counter(collection_area.values())
    combination = (counts['|'], counts['#'])
    results[m] = combination[0] * combination[1]
    combinations_seen[combination].append(m)
    if len(combinations_seen[combination]) > 10:
      combo_times = combinations_seen[combination]
      difference = combo_times[-1] - combo_times[-2]
      iterations_to_final_value = (minutes - m) % difference
      backtrack_value = difference - iterations_to_final_value
      print("Result found via pattern: {0}".format(results[m-backtrack_value]))
      result_found_via_pattern = True
      break
    m += 1
  
  if not result_found_via_pattern:
    counts = Counter(collection_area.values())
    print("Reached final minute, result is {0}".format(counts['|'] * counts['#']))

if __name__ == '__main__':
  main()
