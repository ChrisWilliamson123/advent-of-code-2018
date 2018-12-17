def addr(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = register_states[b]

    result = a_value + b_value
    register_states[output_register] = result
    return register_states

def addi(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = b

    result = a_value + b_value
    register_states[output_register] = result
    return register_states

def mulr(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = register_states[b]

    result = a_value * b_value
    register_states[output_register] = result
    return register_states

def muli(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = b

    result = a_value * b_value
    register_states[output_register] = result
    return register_states

def banr(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = register_states[b]

    result = int(bin(a_value & b_value), 2)
    register_states[output_register] = result
    return register_states

def bani(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = b

    result = int(bin(a_value & b_value), 2)
    register_states[output_register] = result
    return register_states

def borr(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = register_states[b]

    result = int(bin(a_value | b_value), 2)
    register_states[output_register] = result
    return register_states

def bori(register_states, a, b, output_register):
    register_states = register_states.copy()
    a_value = register_states[a]
    b_value = b

    result = int(bin(a_value | b_value), 2)
    register_states[output_register] = result
    return register_states

def setr(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = a
  register_states[output_register] = a_value
  return register_states

def seti(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = register_states[a]
  register_states[output_register] = a_value
  return register_states

def gtir(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = a
  b_value = register_states[b]

  if a_value > b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

def grti(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = register_states[a]
  b_value = b

  if a_value > b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

def gtrr(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = register_states[a]
  b_value = register_states[b]

  if a_value > b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

def eqir(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = a
  b_value = register_states[b]

  if a_value == b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

def eqri(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = register_states[a]
  b_value = b

  if a_value == b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

def eqrr(register_states, a, b, output_register):
  register_states = register_states.copy()
  a_value = register_states[a]
  b_value = register_states[b]

  if a_value == b_value:
    register_states[output_register] = 1
  else:
    register_states[output_register] = 0
  return register_states

all_instruction_functions = [
  addr,
  addi,
  mulr,
  muli,
  banr,
  bani,
  borr,
  bori,
  setr,
  seti,
  gtir,
  grti,
  gtrr,
  eqir,
  eqri,
  eqrr
]