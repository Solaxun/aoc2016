import re

CODE = open('AoC9.txt').read().strip()

def parse_code(code):
	parts =  list(filter(bool,re.split('(\(\d+x\d+\))',code)))
	return parts

def parse_repeats(repeat_seq):
	nextchars,repeats = map(int,repeat_seq.replace('(','').replace(')','')
		.split('x'))
	return nextchars,repeats

def do_repeats(chars,nextchars,times):
	return chars[0:nextchars] * times + chars[nextchars:]

def remove_elements(parts,remove_parts):
	parts = ''.join([elem for part in parts for elem in part])
	for r in remove_parts:
		parts = parts.replace(r,'',1)
	return parts

def decompress(code):
	parts = parse_code(code)
	result = []
	while parts:
		current = parts.pop(0)
		if current.isalpha():
			result.append(current)
		elif current.startswith('('):
			nextchars,times = parse_repeats(current)
			rest_of_parts = ''.join([elem for part in parts[0:] for elem in part])[0:nextchars]
			parts = parse_code(remove_elements(parts,rest_of_parts))
			result.append(do_repeats(rest_of_parts,nextchars,times))

	return ''.join(result)

def decompress2(code):
	if not code: return 0
	parts = parse_code(code)
	first, rest = parts[0],parts[1:]
	rest_of_parts_string = ''.join([elem for l in rest for elem in l])
	if first.isalpha():
		return len(first) + decompress2(rest_of_parts_string)
	elif first.startswith('('):
		nextchars,repeats = parse_repeats(first)
		return (repeats * decompress2(rest_of_parts_string[0:nextchars]) + 
						  decompress2(rest_of_parts_string[nextchars:]))


def part_1(code=CODE):
	return len(decompress(CODE))

def part_2(code=CODE):
	return len(decompress_fully(code,decompress2))

def decompress_fully(code,decompression_func):
	while re.search('(\(\d+x\d+\))',code):
		code = decompression_func(code)
	return code

def test():
	assert(decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG')
	assert(decompress('(6x1)(1x3)A')=='(1x3)A')
	assert(decompress('(3x3)XYZ')=='XYZXYZXYZ')
	assert(decompress('X(8x2)(3x3)ABCY')=='X(3x3)ABC(3x3)ABCY')
	print('tests part 1 pass!')
	assert(decompress_fully('X(8x2)(3x3)ABCY',decompress)=='XABCABCABCABCABCABCY')
	assert(decompress2('(27x12)(20x12)(13x14)(7x10)(1x12)A')==241920) #250 sec for this one
	assert(decompress2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')==445)
	print('tests part 2 pass!')
# test()

print(decompress2(CODE))