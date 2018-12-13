import operator
from collections import defaultdict

DIRECTIONS_TO_STRAIGHTS = {
  '^': '|',
  '>': '-',
  'v': '|',
  '<': '-'
}

DIRECTIONS_TO_COORD_CHANGE = {
  '^': (0, -1),
  '>': (1, 0),
  'v': (0, 1),
  '<': (-1, 0)
}

ROTATE_AT_CURVE = {
  ('^', '/'): '>',
  ('>', '/'): '^',
  ('v', '/'): '<',
  ('<', '/'): 'v',
  ('^', '\\'): '<',
  ('>', '\\'): 'v',
  ('v', '\\'): '>',
  ('<', '\\'): '^',
}

RR = {
  '^': '>',
  '>': 'v',
  'v': '<',
  '<': '^'
}

RL = {
  '^': '<',
  '>': '^',
  'v': '>',
  '<': 'v'
}

def get_next_direction(direction, next_char, next_turn):
  if next_char == '|' or next_char == '-':
    return direction
  if next_char == '/' or next_char == '\\':
    return ROTATE_AT_CURVE[(direction, next_char)]
  if next_turn == 0:
    return RL[direction]
  elif next_turn == 1:
    return direction
  else:
    return RR[direction]

def print_grid(grid):
  max_x = max([x[0] for x in grid.keys()])
  max_y = max([y[1] for y in grid.keys()])
  for y in range(0, max_y+1):
    to_print = ''
    for x in range(0, max_x+1):
      to_print += grid[(x, y)]
    print(to_print)

grid_lines = [x.rstrip('\n') for x in open('input.txt', 'r').readlines()]
grid = defaultdict(tuple)
carts = defaultdict(tuple)
for y, l in enumerate(grid_lines):
    for x, c in enumerate(l):
        if c in DIRECTIONS_TO_STRAIGHTS:
            grid[(x, y)] = DIRECTIONS_TO_STRAIGHTS[c]
            carts[(x, y)] = {
                'direction': c,
                'next_turn': 0
            }
        else:
            grid[(x, y)] = c
print(len(carts))

lengths = defaultdict(int)
prev_carts_len = 20
while len(carts) > 1:
    carts_next_tick = defaultdict(tuple)
    sorted_carts = sorted(carts.keys(), key= lambda x: (x[1], x[0]))
    print(sorted_carts)
    for idx, cart_coord in enumerate(sorted_carts):
        data = carts[cart_coord]
        current_cart_direction = data['direction']
        next_coord = tuple(map(operator.add, cart_coord, DIRECTIONS_TO_COORD_CHANGE[current_cart_direction]))
        last_index = idx == len(sorted_carts) - 1
        if carts_next_tick[next_coord] or next_coord in sorted_carts:
            del carts_next_tick[next_coord]
            print('{0} dead'.format(next_coord))
            continue
        
        next_char = grid[next_coord]
        next_turn = data['next_turn']
        next_direction = get_next_direction(current_cart_direction, next_char, next_turn)
        next_cart_data = {
            'direction': next_direction,
            'next_turn': ((next_turn + 1) % 3) if next_char == '+' else next_turn,
        }
        carts_next_tick[next_coord] = next_cart_data
        sorted_carts[idx] = (-1, -1)
    carts = carts_next_tick
    lengths[len(carts)] += 1
    if len(carts) != prev_carts_len:
        # print(sorted(carts.keys()))
        prev_carts_len = len(carts)
    
print(lengths)
print(carts.keys())