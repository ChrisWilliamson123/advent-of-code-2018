import sys
from collections import defaultdict

def parse_state(initial_state_text):
  state = defaultdict(int)
  for idx, pot in enumerate(initial_state_text.split()[-1]):
    if pot == '#':
      state[idx] = True
      
  return state

def parse_rules(rules):
  rules_dict = defaultdict(str)
  for r in rules:
    r_split = r.split(' => ')
    rules_dict[r_split[0]] = r_split[1]
  return rules_dict

def build_pots_string(pot_index, state):
  result = ''
  for i in range(pot_index-2, pot_index+3):
    result += '#' if state[i] else '.'
  return result

def get_plant_min_max(state):
  mi = 100
  ma = -100
  for key in state.keys():
    if key < mi:
      mi = key
    if key > ma:
      ma = key
  return (mi, ma)

def main():
  input_lines = [l.rstrip() for l in open('input.txt', 'r').readlines()]
  state = parse_state(input_lines[0])
  rules = parse_rules(input_lines[2:])
  min_index, max_index = get_plant_min_max(state)
  last_sums = [0]
  
  for i in range(0, int(sys.argv[1])):
    new_state = defaultdict(int)
    indexes = set()
    for pot in state.keys():
      for i in range(pot-2, pot+3):
        indexes.add(i)
    for pot_index in indexes:
      surrounding_pots = build_pots_string(pot_index, state)
      rule_result = rules[surrounding_pots]
      if rule_result == '#':
        new_state[pot_index] = '#'
        if pot_index < min_index:
          min_index = pot_index
        elif pot_index > max_index:
          max_index = pot_index
    state = new_state
    state_sum = sum(state.keys())
    print(state_sum - last_sums[-1])
    last_sums.append(state_sum)
  print(last_sums[-1])

if __name__ == '__main__':
  main()
