import string
import operator

remove_units_from_polymer = lambda p, i: p[:i] + p[i+2:]

def react_polymer(polymer):
  index = 0
  while index < len(polymer)-1:
    current_unit = polymer[index]
    next_unit = polymer[index+1]

    if next_unit.swapcase() == current_unit:
      polymer = remove_units_from_polymer(polymer, index)
      index = index - 1 if index != 0 else 0
    else:
      index += 1

  return polymer

def main():
  polymer = open('input.txt', 'r').readline()
  
  letters = list(string.ascii_lowercase)
  letters_to_poly_length = {}
  
  for l in letters:
    cleansed_polymer = polymer.replace(l, '').replace(l.upper(), '')
    reacted_polymer = react_polymer(cleansed_polymer)
    letters_to_poly_length[l] = len(reacted_polymer)
  
  print(min(letters_to_poly_length.values()))

if __name__ == '__main__':
  main()
