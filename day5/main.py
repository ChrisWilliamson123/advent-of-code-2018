remove_units_from_polymer = lambda p, i: p[:i] + p[i+2:]

def main():
  polymer = open('input.txt', 'r').readline()
  index = 0
  while index < len(polymer)-1:
    current_unit = polymer[index]
    next_unit = polymer[index+1]

    if next_unit.swapcase() == current_unit:
      polymer = remove_units_from_polymer(polymer, index)
      index = index - 1 if index != 0 else 0
    else:
      index += 1

  print(len(polymer))

if __name__ == '__main__':
  main()
