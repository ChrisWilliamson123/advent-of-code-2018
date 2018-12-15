def main():
  box_ids = sorted([x.rstrip() for x in open('input.txt', 'r').readlines()])
  for index, box_id in enumerate(box_ids):
    for j in range(0, index):
      characters_different = 0
      differing_char = ''
      for char_index in range(0, len(box_id)):
        if box_id[char_index] != box_ids[j][char_index]:
          characters_different += 1
          differing_char = box_id[char_index]
      if characters_different == 1:
        print(box_id)
        print(differing_char)
        return
if __name__ == '__main__':
  main()