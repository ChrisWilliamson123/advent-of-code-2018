import operator
from collections import defaultdict

def parse_cave(cave_text):
  cave = defaultdict(tuple)
  elves = defaultdict(tuple)
  goblins = defaultdict(tuple)
  for y, l in enumerate(cave_text):
    for x, c in enumerate(l):
      coord = (x, y)
      if c != '#':
        cave[coord] = c
      if c == 'E':
        elves[coord] = {
          'hp': 200
        }
      elif c == 'G':
        goblins[coord] = {
          'hp': 200
        }
  return cave, elves, goblins

def get_adjacent_squares(p):
  return [
    (p[0], p[1]-1),
    (p[0], p[1]+1),
    (p[0]-1, p[1]),
    (p[0]+1, p[1])
  ]

def get_open_squares(target, cave):
  open_squares = []
  to_check = get_adjacent_squares(target)
  for c in to_check:
    if cave[c] == '.':
      open_squares.append(c)
  return open_squares

def get_close_enemies(targets, adjacent_squares):
  close_enemies = []
  for t in targets:
    if t in adjacent_squares:
      close_enemies.append(t)
  return close_enemies

def get_shortest_distance(origin, target, cave, distance, visited):
  visited.append(origin)
  adjacent_squares = get_adjacent_squares(origin)
  if target in adjacent_squares:
    return distance, origin
  
  open_squares = []
  for c in adjacent_squares:
    if cave[c] == '.' and c not in visited:
      open_squares.append(c)
  if not open_squares:
    return 10000, (1000, 1000)

  distances = []
  visited_len = len(visited)
  for c in open_squares:
    # if c == (4, 5):
    #   print('here')
    shortest_distance, coord = get_shortest_distance(c, target, cave, distance+1, visited)
    distances.append((shortest_distance, coord))
    visited = visited[0:visited_len+1]
  sorted_distances = sorted(distances, key=lambda d: (d[0], d[1][1], d[1][0]))
  minimum = sorted_distances[0]
  return minimum

def main():
  attack_power = 3
  hit_points = 200
  cave_text = [l.rstrip() for l in open('input.txt', 'r').readlines()]
  cave, elves, goblins = parse_cave(cave_text)
  print('Starting elves: {0}'.format(elves))
  print('Starting goblins: {0}'.format(goblins))

  elf_coords = list(elves.keys())
  goblin_coords = list(goblins.keys())

  player_positions = sorted(
    elf_coords + goblin_coords,
    key=lambda x: (x[1], x[0])
  )

  end = False
  rounds = 0

  while not end:
    index = 0
    while index < len(player_positions):
      pos = player_positions[index]
      adjacent_squares = get_adjacent_squares(pos)
      is_elf = pos in elves
      if is_elf:
        enemies = goblins
        possible_targets = goblin_coords
      else:
        enemies = elves
        possible_targets = elf_coords

      if len(possible_targets) == 0:
        print("No more targets!")
        end = True
        elves_win = is_elf
        break
      
      close_enemies = get_close_enemies(possible_targets, adjacent_squares)
      if close_enemies:
        # print("Enemy(s) close")
        # print(close_enemies, enemies)
        sorted_by_health = sorted(close_enemies, key=lambda x: (enemies[x]['hp'], x[1], x[0]))
        enemy_to_attack = sorted_by_health[0]
        enemies[enemy_to_attack]['hp'] -= attack_power
        if enemies[enemy_to_attack]['hp'] <= 0:
          cave[enemy_to_attack] = '.'
          del enemies[enemy_to_attack]
          if is_elf:
            # print("Goblin at {0} dead".format(enemy_to_attack))
            goblin_coords = list(goblins.keys())
          else:
            # print("Elf at {0} dead".format(enemy_to_attack))
            elf_coords = list(elves.keys())
          player_pos_index = player_positions.index(enemy_to_attack)
          player_positions.pop(player_pos_index)
          if player_pos_index > index:
            index += 1
        else:
          index += 1
        continue

      open_squares_around_targets = []
      for t in possible_targets:
        open_squares_around_targets += get_open_squares(t, cave)
      if not open_squares_around_targets:
        # print('No possible squares around targets.')
        index += 1
        continue

      shortest_distances = []
      for c in open_squares_around_targets:
        print('Working out distance between {0} and {1}'.format(c, pos))
        result = get_shortest_distance(c, pos, cave, 0, [])
        shortest_distances.append(result)
      to_move_to = sorted(shortest_distances, key=lambda d: (d[0], d[1][1], d[1][0]))[0][1]
      if to_move_to != (1000, 1000):
        if is_elf:
          current = elves[pos]
          cave[pos] = '.'
          elves[to_move_to] = current
          cave[to_move_to] = 'E'
          del elves[pos]
          elf_coords = list(elves.keys())
        else:
          current = goblins[pos]
          cave[pos] = '.'
          goblins[to_move_to] = current
          cave[to_move_to] = 'G'
          del goblins[pos]
          goblin_coords = list(goblins.keys())
        player_positions[index] = to_move_to

      adjacent_squares = get_adjacent_squares(player_positions[index])
      close_enemies = get_close_enemies(possible_targets, adjacent_squares)
      if close_enemies:
        # print("Enemy(s) close")
        # print(close_enemies, enemies)
        sorted_by_health = sorted(close_enemies, key=lambda x: (enemies[x]['hp'], x[1], x[0]))
        enemy_to_attack = sorted_by_health[0]
        enemies[enemy_to_attack]['hp'] -= attack_power
        if enemies[enemy_to_attack]['hp'] <= 0:
          cave[enemy_to_attack] = '.'
          del enemies[enemy_to_attack]
          if is_elf:
            # print("Goblin at {0} dead".format(enemy_to_attack))
            goblin_coords = list(goblins.keys())
          else:
            # print("Elf at {0} dead".format(enemy_to_attack))
            elf_coords = list(elves.keys())
          player_pos_index = player_positions.index(enemy_to_attack)
          player_positions.pop(player_pos_index)
          if player_pos_index > index:
            index += 1
        else:
          index += 1
        continue

      index += 1
    # print('\n')
    rounds += 1
    print(rounds)
    player_positions = sorted(player_positions, key=lambda x: (x[1], x[0]))
    # print(rounds)
    # for coord, data in goblins.items():
    #   print(coord, data['hp'])
    # for coord, data in elves.items():
    #   print(coord, data['hp'])
  print(goblins)
  print(elves)
  print(rounds)


  
  # for coord in sorted(cave.keys(), key=lambda c: (c[1], c[0])):
    


if __name__ == '__main__':
  main()
