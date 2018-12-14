from collections import defaultdict

def main():
  frequencies = [int(f) for f in open('input.txt', 'r').readlines()]
  frequencies_reached = defaultdict(int)
  frequencies_reached[0] = 1
  latest_f = 0

  found = False
  f_index = 0
  while not found:
    next_f = latest_f + frequencies[f_index]
    if frequencies_reached[next_f]:
      found = True
      print(next_f)
    else:
      latest_f = next_f
      frequencies_reached[next_f] = 1
      f_index = f_index + 1 if f_index + 1 < len(frequencies) else 0

if __name__ == '__main__':
  main()
