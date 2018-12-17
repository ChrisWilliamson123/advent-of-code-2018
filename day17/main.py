import re
import operator
from collections import defaultdict, namedtuple

class Point(namedtuple('Point', 'x y')):
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

SPRING = Point(500, 0)
UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

def parse_clay(clay):
  positions = defaultdict(int)
  for entry in clay:
    single_coord_index = 0 if entry[0] == 'x' else 1
    single, range_start, range_end = [int(n) for n in re.findall('\d+', entry)]
    for c in range(range_start, range_end+1):
      coord = [0, 0]
      coord[single_coord_index] = single
      coord[int(not single_coord_index)] = c
      positions[tuple(coord)] = 1
  return positions

def is_blocked_left(origin, clay_positions, settled_positions):
  one_left = (origin[0]-1, origin[1])
  one_left_below = (one_left[0], one_left[1]+1)
  while clay_positions[one_left_below] or settled_positions[one_left_below]:
    if clay_positions[one_left]:
      return (True, origin[0] - one_left[0])
    one_left = (one_left[0]-1, one_left[1])
    one_left_below = (one_left[0], one_left[1]+1)
  return (False, origin[0] - one_left[0])

def is_blocked_right(origin, clay_positions, settled_positions):
  one_right = (origin[0]+1, origin[1])
  one_right_below = (one_right[0], one_right[1]+1)
  while clay_positions[one_right_below] or settled_positions[one_right_below]:
    if clay_positions[one_right]:
      return (True, one_right[0] - origin[0])
    one_right = (one_right[0]+1, one_right[1])
    one_right_below = (one_right[0], one_right[1]+1)
  return (False, one_right[0] - origin[0])

def print_map(clay, flowing, still, x1=300, x2=700, y1=0, y2=1000):
  def char(p):
    if p == SPRING:
      return '+'
    elif p in clay:
      return '#'
    elif p in both:
      return '~' # For water that is tagged as both flowing and still
    elif p in still:
      return '~'
    elif p in flowing:
      return '|'
    else:
      return '.'

  both = flowing & still
  print('\n'.join(''.join(char(Point(x, y)) for x in range(x1, 1 + x2)) for y in range(y1, 1 + y2)))

def main():
  clay_input = [l.rstrip() for l in open('input.txt', 'r').readlines()]
  clay_positions = parse_clay(clay_input)
  
  water_positions = defaultdict(int)
  settled_positions = defaultdict(int)
  current_water_flowing_positions = {(500, 0)}
  max_y = max(clay_positions.keys(), key=lambda x: x[1])[1]
  print(max_y)
  min_y = min(clay_positions.keys(), key=lambda x: x[1])[1]

  while max(current_water_flowing_positions, key=lambda x: x[1])[1] < max_y:
    new_positions = set()

    for pos in current_water_flowing_positions:
      one_below = (pos[0], pos[1]+1)

      if not clay_positions[one_below] and not settled_positions[one_below]:
        new_positions.add(one_below)
        water_positions[one_below] = 1
        continue

      blocked_left_amount = is_blocked_left(pos, clay_positions, settled_positions)
      blocked_right_amount = is_blocked_right(pos, clay_positions, settled_positions)
      if blocked_left_amount[0] and blocked_right_amount[0]:
        for x in range(pos[0]-(blocked_left_amount[1]-1), pos[0]+1):
          settled_positions[(x, pos[1])] = 1
        for x in range(pos[0]+1, pos[0]+blocked_right_amount[1]):
          settled_positions[(x, pos[1])] = 1
        one_above = (pos[0], pos[1]-1)
        
        new_positions.add(one_above)
        continue

      for x in range(pos[0]-(blocked_left_amount[1]-1), pos[0]+1):
        water_positions[(x, pos[1])] = 1
      if not blocked_left_amount[0]:
        water_positions[(pos[0]-blocked_left_amount[1], pos[1])] = 1
        new_positions.add((pos[0]-blocked_left_amount[1], pos[1]))
      for x in range(pos[0]+1, pos[0]+blocked_right_amount[1]+1):
        water_positions[(x, pos[1])] = 1
      if not blocked_right_amount[0]:
        new_positions.add((pos[0]+blocked_right_amount[1], pos[1]))
    
    current_water_flowing_positions = new_positions

  flowing_coords = sorted(
    [coord for coord, active in water_positions.items() if active],
    key=lambda c: (c[1], c[0])
  )

  settled_coords = sorted(
    [coord for coord, active in settled_positions.items() if active],
    key=lambda c: (c[1], c[0])
  )

  clay_coords = [coord for coord, active in clay_positions.items() if active]

  print_map(set(clay_coords), set(flowing_coords), set(settled_coords), y1=min_y, y2=max_y)


if __name__ == '__main__':
  main()
