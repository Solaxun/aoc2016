"""cpy x y copies x (either an integer or the value of a register) into register y.
inc x increases the value of register x by one.
dec x decreases the value of register x by one.
jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero"""


instr = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".split('\n')

real_instr = """cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 19 c
cpy 14 d
inc a
dec d
jnz d -2
dec c
jnz c -5""".split('\n')

registers = {'a':0,'b':0,'c':1,'d':0}

operations = {'cpy':lambda val, r: int(val) if val.isdigit() else registers[val],
			  'inc':lambda r: registers[r] + 1,
			  'dec':lambda r: registers[r] - 1,
			  'jnz':lambda r,offset: int(offset) if registers.get(r,r) else None} 

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

print(registers)