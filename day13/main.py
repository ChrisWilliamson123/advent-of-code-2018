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



def parse_grid(lines):
  grid = defaultdict(tuple)
  carts = defaultdict(tuple)
  for y, l in enumerate(lines):
    for x, c in enumerate(l):
      grid[(x, y)] = c
      if c == '^' or c == '>' or c == 'v' or c == '<':
        carts[(x, y)] = {
          'direction': c,
          'next_turn': 1,
          'track_piece': '|' if c == '^' or c == 'v' else '-'
        }
  return (grid, carts)

# def get_next_coord(current_coord, direction, next_turn, grid):
def get_next_direction(direction, next_char, next_turn):
  if next_char == '|' or next_char == '-':
    return direction
  if next_char == '/' or next_char == '\\':
    return ROTATE_AT_CURVE[(direction, next_char)]
  turn_type = next_turn
  if turn_type == 1:
    return RL[direction]
  elif turn_type == 2:
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

def main():
  grid, carts = parse_grid([x.rstrip('\n') for x in open('input.txt', 'r').readlines()])
  lengths = defaultdict(int)
  # print_grid(grid)
  while len(carts) > 3:
    next_carts = defaultdict(tuple)
    next_grid_changes = defaultdict(tuple)
    for cart_coord, data in carts.items():
      # print(len(carts))
      direction = data['direction']
      # print('Direction: {0}'.format(direction))
      next_coord = tuple(map(operator.add, cart_coord, DIRECTIONS_TO_COORD_CHANGE[data['direction']]))
      # print('Next coord: {0}'.format(next_coord))
      if next_carts[next_coord]:
        next_grid_changes[next_coord] = next_carts[next_coord]['track_piece']
        next_grid_changes[cart_coord] = data['track_piece']
        del next_carts[next_coord]
        continue
        # print(next_coord)
      next_char = grid[next_coord]
      # print('Next char: {0}'.format(next_char))
      next_direction = get_next_direction(direction, next_char, data['next_turn'])
      # print('Next direction: {0}'.format(next_direction))

      next_cart_data = {
        'direction': next_direction,
        'next_turn': ((data['next_turn'] + 1) % 3)if next_char == '+' else data['next_turn'],
        'track_piece': next_char
      }
      # print('Next cart data: {0}'.format(next_cart_data))
      next_carts[next_coord] = next_cart_data
      next_grid_changes[next_coord] = next_cart_data['direction']
      next_grid_changes[cart_coord] = data['track_piece']

      # print(cart_coord, direction, next_coord, next_char, next_direction)
      # print(len(carts))
    # print('Next carts: {0}'.format(next_carts))
    # print('Grid changes: {0}'.format(next_grid_changes))
    for coord, char in next_grid_changes.items():
      grid[coord] = char
    carts = next_carts
    # print_grid(grid)
    lengths[len(carts)] += 1
  print(lengths)
  print(carts.keys())

if __name__ == '__main__':
  main()
