from collections import Counter, defaultdict

def parse_claim(claim):
  split = claim.split(' ')
  id = int(split[0].replace('#', ''))
  origin = tuple([int(x) for x in split[2].replace(':', '').split(',')])
  area = tuple([int(x) for x in split[-1].split('x')])
  return (id, origin, area)

def main():
  fabric_input = [l.rstrip() for l in open('input.txt', 'r').readlines()]
  coords_to_ids = defaultdict(tuple)
  all_ids = set()
  dupe_ids = set()
  dupe_coords = set()

  for c in fabric_input:
    id, origin, area = parse_claim(c)
    all_ids.add(id)
    for x in range(origin[0], origin[0]+area[0]):
      for y in range(origin[1], origin[1]+area[1]):
        coord = (x, y)
        if coords_to_ids[coord]:
          coords_to_ids[coord].append(id)
          for dupe_id in coords_to_ids[coord]:
            dupe_ids.add(dupe_id)
          dupe_coords.add(coord)
        else:
          coords_to_ids[coord] = [id]

  print(len(dupe_coords))
  print(list(all_ids-dupe_ids)[0])

if __name__ == '__main__':
  main()
