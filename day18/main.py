from collections import defaultdict, Counter

def parse_input(input_lines):
  area = defaultdict(str)
  for y, l in enumerate(input_lines):
    for x, c in enumerate(l):
      area[(x, y)] = c
  return area, len(input_lines)-1

def get_adjacent_coords(origin, edge):
  origin_x = origin[0]
  origin_y = origin[1]
  adjacents = []
  for x in range(origin_x-1, origin_x+2):
    if 0 <= x <= edge:
      for y in range(origin_y-1, origin_y+2):
        if 0 <= y <= edge and (x, y) != origin:
          adjacents.append((x, y))
  return adjacents

def get_contents_of_coords(coords, collection_area):
  values = [collection_area[co] for co in coords]
  return Counter(values)

def print_area(collection_area, max_edge):
  for y in range(max_edge+1):
    to_print = ''
    for x in range(max_edge+1):
      to_print += collection_area[(x, y)]
    print(to_print)

def main():
  collection_area, max_edge = parse_input([l.rstrip() for l in open('input.txt', 'r').readlines()])
  minutes = 1000000000
  
  for m in range(minutes):
    new_collection_area = defaultdict(str)
    for coord, content in collection_area.items():
      adjacent_coords = get_adjacent_coords(coord, max_edge)
      content_counts = get_contents_of_coords(adjacent_coords, collection_area)
      if content == '.' and content_counts['|'] >= 3:
        new_collection_area[coord] = '|'
      elif content == '|' and content_counts['#'] >= 3:
        new_collection_area[coord] = '#'
      elif content == '#':
        if content_counts['#'] >= 1 and content_counts['|'] >= 1:
          new_collection_area[coord] = content
        else:
          new_collection_area[coord] = '.'
      else:
        new_collection_area[coord] = content
    collection_area = new_collection_area
    counts = Counter(collection_area.values())
    print(m, counts['|'], counts['#'], counts['|'] * counts['#'])

  

if __name__ == '__main__':
  main()
