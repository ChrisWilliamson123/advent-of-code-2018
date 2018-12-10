import operator, sys
from collections import defaultdict

def parse_input():
  split = open('input.txt', 'r').readline().split()
  return (int(split[0]), int(split[-2]))

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def main():
  players = int(sys.argv[1])
  last_marble = int(sys.argv[2])

  scores = defaultdict(int)
  circle = [0]
  current_index = 0

  for marble in range(1, last_marble+1):
    if marble % 23 == 0:
      scores[marble % players] += marble
      index_to_remove = current_index - 7
      if index_to_remove < 0:
        index_to_remove = len(circle) - abs(index_to_remove)
      scores[marble % players] += circle[index_to_remove]
      circle.pop(index_to_remove)
      current_index = index_to_remove
    else:
      one_clockwise_index = current_index + 1
      if one_clockwise_index == len(circle):
        one_clockwise_index = 0
      two_clockwise_index = one_clockwise_index + 1
      if two_clockwise_index == len(circle):
        circle.append(marble)
      else:
        circle.insert(two_clockwise_index, marble)
      current_index = two_clockwise_index
    sys.stdout.flush()
    restart_line()
    sys.stdout.write('{0}'.format(marble))
    sys.stdout.flush()
    

  
  print(max(scores.items(), key=operator.itemgetter(1)))
  
      
    

if __name__ == '__main__':
  main()
