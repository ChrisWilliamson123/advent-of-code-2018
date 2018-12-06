from collections import defaultdict, Counter

def get_coords_min_max(coords):
  x_values = []
  y_values = []
  for c in coords:
    x_values.append(c[0])
    y_values.append(c[1])
  return (
    min(x_values),
    max(x_values),
    min(y_values),
    max(y_values)
  )

def manhattan_distance(co1, co2):
  return abs(co2[0] - co1[0]) + abs(co2[1] - co1[1])

def main():
  coords = set([tuple(map(int, c.rstrip().split(', '))) for c in open('input.txt', 'r').readlines()])
  min_x, max_x, min_y, max_y = get_coords_min_max(coords)
  ids_to_coords = {coord_id: coord for coord_id, coord in enumerate(coords, start=1)}

  areas = defaultdict(int)
  invalid_ids = set()
  
  for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
      # Format is [(distance, id), (distance, id)]
      shortest_distances = sorted([(manhattan_distance(co1, (x, y)), id) for id, co1 in ids_to_coords.items()], key=lambda x: x[0])
      if shortest_distances[0][0] != shortest_distances[1][0]:
        areas[shortest_distances[0][1]] += 1
        if x == min_x or x == max_x or y == min_y or y == max_y:
          invalid_ids.add(shortest_distances[0][1])
  
  print(max(size for id, size in areas.items() if id not in invalid_ids))

def total_distance(x, y, coords):
  total = 0
  for c in coords:
    d = manhattan_distance((x, y), c)
    total += d
  return total

def part_two():
  coords = set([tuple(map(int, c.rstrip().split(', '))) for c in open('input.txt', 'r').readlines()])
  min_x, max_x, min_y, max_y = get_coords_min_max(coords)
  region_size = 0
  for x in range(min_x, max_x+1):
    for y in range(min_y, max_y+1):
      distance = total_distance(x, y, coords)
      if distance < 10000:
        region_size += 1
  print(region_size)


  
if __name__ == '__main__':
  part_two()
