def calculate_power_level(cell, grid_serial_number):
  rack_id = cell[0] + 10
  power_level = rack_id * cell[1]
  power_level += grid_serial_number
  power_level *= rack_id
  power_level = ((power_level // 100) % 10) - 5
  return power_level

def calculate_total_power(origin, size, power_grid):
  x_coord = origin[0]
  y_coord = origin[1]
  total_power = 0
  for x in range(x_coord, x_coord+size):
    for y in range(y_coord, y_coord+size):
      total_power += power_grid[(x, y)]
  return total_power

def main():
  grid_serial_number = 9798
  # grid_serial_number = 18
  max_power = 0
  max_power_origin = (0, 0)
  max_power_grid_size = 0
  power_grid = {}
  totals = {}

  for y in range(1, 300+1):
    for x in range(1, 300+1):
      cell = (x, y)
      power_grid[cell] = calculate_power_level(cell, grid_serial_number)
      totals[cell] = 0

  
  for size in range(1, 300+1):
    print(size)
    for row in range(size, 300+1):
      for col in range(size, 300+1):
        origin = (row - (size-1), col - (size - 1))
        # print('Calculating total power for ({0},{1}) size {2}'.format(origin[0], origin[1], size))
        boundary_coords = set()
        for x in range(origin[0], origin[0]+size):
          boundary_coords.add((x, origin[1]+(size-1)))
        for y in range(origin[1], origin[1]+size):
          boundary_coords.add((origin[0]+(size-1), y))

        boundary_total = 0
        for b in boundary_coords:
          boundary_total += power_grid[b]

        total_power = boundary_total + totals[origin]
        totals[origin] = total_power
        if total_power > max_power:
          max_power = total_power
          max_power_origin = origin
          max_power_grid_size = size
  print(max_power, max_power_origin, max_power_grid_size)



if __name__ == '__main__':
  main()
