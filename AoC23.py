INSTRUCTIONS = """cpy a b
dec b
cpy a d
cpy 0 a
cpy b c
inc a
dec c
jnz c -2
dec d
jnz d -5
dec b
cpy b c
cpy c d
dec d
inc c
jnz d -2
tgl c
cpy -16 c
jnz 1 c
cpy 75 c
jnz 85 d
inc a
inc d
jnz d -2
inc c
jnz c -5""".split('\n')

#a = 7 for part 1... takes a few minutes, part 2 was overnight so need to optimize
REGISTERS = {'a':12,'b':0,'c':0,'d':0}

def jnz(r,offset):
	 r = int(r) if r.isdigit() else REGISTERS[r]
	 offset = int(offset) if offset.replace('-','',1).isdigit() else REGISTERS[offset]
	 return offset if r else None

operations = {'cpy':lambda val, r: int(val) if val.replace('-','',1).isdigit() else REGISTERS[val],
			  'inc':lambda r: REGISTERS[r] + 1,
			  'dec':lambda r: REGISTERS[r] - 1,
			  'jnz':jnz,
			  'tgl':lambda offset: int(offset) if offset.isdigit() else REGISTERS[offset]}

transition = {'cpy':'jnz',
              'jnz':'cpy',
              'inc':'dec',
              'dec':'inc',
              'tgl':'inc'}

def parse_instruction(instructions):
	op, *args = instructions.split()
	func = operations[op]
	if op == 'jnz':
		return func(*args),False
	elif op == 'tgl':
		return func(*args),True 
	else:
		if op == 'cpy' and args[1] not in REGISTERS: return False,False
		r = get_register(*args)
		REGISTERS[r] = func(*args)
		return False,False

def get_register(*args):
	return [arg for arg in args if arg in 'abcd'][-1]

def make_new_instruction(op,args):
	new_op = transition[op]
	return str(new_op) + ' ' + ' '.join(args)

def solve(instructions):
	global REGISTERS
	position = 0
	while position < len(instructions):
		jump,istgl = parse_instruction(instructions[position])
		if jump and not istgl:
			position += jump
		elif istgl:
			pos = position + jump
			if 0 <= pos < len(instructions):
				inst_to_tgl = instructions[pos]
				op, *args = inst_to_tgl.split()
				instructions[pos] = make_new_instruction(op,args)
				position += 1
			else:
				position += 1
		else:
			position += 1
	return REGISTERS	

print(solve(INSTRUCTIONS))