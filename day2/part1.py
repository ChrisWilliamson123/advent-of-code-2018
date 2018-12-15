from collections import Counter

def main():
  box_ids = [x.rstrip() for x in open('input.txt', 'r').readlines()]
  ids_to_letter_counts = {}
  two_letter_count = 0
  three_letter_count = 0
  for id in box_ids:
    letter_counts = Counter(id).values()
    if 2 in letter_counts:
      two_letter_count += 1
    if 3 in letter_counts:
      three_letter_count += 1
  print(two_letter_count * three_letter_count)

if __name__ == '__main__':
  main()
