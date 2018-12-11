import operator, re
from collections import defaultdict

def get_x_y_boundaries(positions):
  x_values = [x[0] for x in positions]
  y_values = [y[1] for y in positions]
  min_x = min(x_values)
  max_x = max(x_values)
  min_y = min(y_values)
  max_y = max(y_values)
  return ([min_x, max_x], [min_y, max_y])

def is_word(positions):
  x_bound, y_bound = get_x_y_boundaries(positions)
  if y_bound[1] - y_bound[0] < 10:
    return True
  return False

def move_positions(positions):
  new_positions = []
  for p in positions:
    pos = p[0]
    v = p[1]
    new_pos = tuple(map(operator.add, pos, v))
    new_positions.append((new_pos, v))
  return new_positions

def print_word(positions):

  x_bound, y_bound = get_x_y_boundaries(positions)
  for y in range(y_bound[0], y_bound[1]+1):
    # print(y)
    to_print = ''
    for x in range(x_bound[0], x_bound[1]+1):
      # print(x)
      if (x, y) in positions:
        to_print += '#'
      else:
        to_print += '.'
    print(to_print)



def main():
  points = [l.rstrip() for l in open('input.txt', 'r').readlines()]
  positions = []

  for p in points:
    numbers = [int(n) for n in re.findall('(-*\d+)', p)]
    positions.append(([numbers[0], numbers[1]], [numbers[2], numbers[3]]))

  elapsed = 0
  while not is_word([p[0] for p in positions]):
    positions = move_positions(positions)
    elapsed += 1
  
  print_word([p[0] for p in positions])
  print(elapsed)

if __name__ == '__main__':
  main()
