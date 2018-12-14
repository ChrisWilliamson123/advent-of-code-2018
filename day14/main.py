def get_new_recipes(score):
  return list(map(int, str(score)))

def change_recipe(current_index, scores):
  amount_to_move = scores[current_index] + 1
  new_index = current_index + amount_to_move
  if new_index > len(scores) - 1:
    new_index = new_index % len(scores)
  return new_index

def perform_round(scores, elf_1_index, elf_2_index):
  combined_recipe_score = scores[elf_1_index] + scores[elf_2_index]
  new_recipes = get_new_recipes(combined_recipe_score)
  
  scores += new_recipes

  elf_1_index = change_recipe(elf_1_index, scores)
  elf_2_index = change_recipe(elf_2_index, scores)

  return (scores, elf_1_index, elf_2_index)

def input_found(scores, input, input_length):
  return scores[-input_length:] == input or scores[-input_length-1:-1] == input

def main():
  recipe_input_str = '440231'
  recipe_input_list = list(map(int, recipe_input_str))
  recipe_input_list_len = len(recipe_input_list)

  elf_1_cr_index = 0
  elf_2_cr_index = 1

  recipe_scores = [3, 7]

  while not input_found(recipe_scores, recipe_input_list, recipe_input_list_len):
    recipe_scores, elf_1_cr_index, elf_2_cr_index = perform_round(
      recipe_scores,
      elf_1_cr_index,
      elf_2_cr_index
    )
  scores_length = len(recipe_scores)
  answer = scores_length - recipe_input_list_len if recipe_scores[-1] == recipe_input_list[-1] else scores_length - recipe_input_list_len - 1
  print(answer)

if __name__ == '__main__':
  main()
