real_instr = """cpy a d
cpy 11 c
cpy 231 b
inc d
dec b
jnz b -2
dec c
jnz c -5
cpy d a
jnz 0 0
cpy a b
cpy 0 a
cpy 2 c
jnz b 2
jnz 1 6
dec b
dec c
jnz c -4
inc a
jnz 1 -7
cpy 2 b
jnz c 2 #need c as 1 here
jnz 1 4
dec b
dec c
jnz 1 -4
jnz 0 0
out b
jnz a -19
jnz 1 -21""".split('\n')

registers = {'a':5,'b':0,'c':0,'d':0}

operations = {'cpy':lambda val, r: int(val) if val.isdigit() else registers[val],
              'inc':lambda r: registers[r] + 1,
              'dec':lambda r: registers[r] - 1,
              'jnz':lambda r,offset: int(offset) if registers.get(r,r) else None,
              'out':lambda val: print(int(val)) if val.isdigit() else print(registers[val])} 

def parse_instruction(inst):
    op, *args = inst.split()
    func = operations[op]
    if op == 'jnz':
        return func(*args)
    else:
        r = get_register(*args)
        registers[r] = func(*args)

def get_register(*args):
    return [arg for arg in args if arg in 'abcd'][-1]

position = 0

while position < len(real_instr):
    jump = parse_instruction(real_instr[position])
    if jump:
        position += jump
    else:
        position += 1

