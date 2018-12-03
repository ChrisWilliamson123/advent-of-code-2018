def main():
  resulting_frequency = sum([int(f) for f in open('input.txt', 'r').readlines()])
  print(resulting_frequency)

if __name__ == '__main__':
  main()
