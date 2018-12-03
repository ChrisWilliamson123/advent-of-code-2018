def main():
  frequencies = [int(f) for f in open('input.txt', 'r').readlines()]
  current_freq = 0
  results = [0]
  freq_index = 0

  while True:
    current_freq += frequencies[freq_index] 
    if current_freq in results:
      print(current_freq)
      break
    results.append(current_freq)
    freq_index = freq_index + 1 if freq_index < len(frequencies) - 1 else 0

    
  

if __name__ == '__main__':
  main()
