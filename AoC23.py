"""cpy x y copies x (either an integer or the value of a register) into register y.
inc x increases the value of register x by one.
dec x decreases the value of register x by one.
jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero"""


instr = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a""".split('\n') #3 should be left in reg a for this input

real_instr = """cpy a b
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

def parse_instruction(inst):
	op, *args = inst.split()
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

def solve(instructions=instr):
	global REGISTERS
	position = 0
	while position < len(instructions):
		# print(instructions[position],'| pos = ',position)
		jump,istgl = parse_instruction(instructions[position])
		# if istgl:print(jump,position+jump)
		if jump and not istgl:
			position += jump
		elif istgl:
			# print('yes')
			pos = position + jump
			if 0 <= pos < len(instructions):
				inst_to_tgl = instructions[pos]
				# print(pos)
				# print('*',inst_to_tgl)
				op, *args = inst_to_tgl.split()
				instructions[pos] = make_new_instruction(op,args)
				position += 1
			else:
				position += 1
		else:
			position += 1
		# print(REGISTERS)
		# print(instructions)
	return REGISTERS	

# REGISTERS = dict(a=0,b=0,c=0,d=0)
# test = """cpy 2 a
# tgl b
# cpy a d
# inc d
# dec a
# tgl d
# dec d
# jnz d -1
# jnz a -6""".split('\n')

print(solve(instructions=real_instr))



"""tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):

For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.

If an attempt is made to toggle an instruction outside the program, nothing happens.
If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a),resulting inst not exec til next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

cpy 2 a initializes register a to 2.
The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
The fourth line, which is now inc a, increments a to 3.
Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.
In this example, the final value in register a is 3.
"""


