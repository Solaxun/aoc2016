"""The document goes on to explain that each button to be pressed can be found by starting on 
the previous button and moving to adjacent buttons on the keypad: U moves up, D moves down, 
L moves left, and R moves right
 Each line of instructions corresponds to one button, starting at the previous button (or, for the first line, the "5" button);
 press whatever button you're on at the end of each line. If a move doesn't lead to a button, ignore it and go till index ends

"""
import math

DIRS = {'U':-5,'D':5,'L':-1,'R':1}
DIRS_DIAMOND = {'U':-7,'D':7,'L':-1,'R':1}

MOVES2 = """
ULL
RRDDD
LURDL
UUUUD
""".strip()
MOVES = open('AoC2.txt').read()
KEYPAD = """123456789"""

def add_borders_to(keypad=KEYPAD):
	top = bottom = '|' * (3 + 1)
	return (top + 
	''.join(['|' + keypad[i:i+3] + '|' for i in range(0,len(keypad),3)]) +
	 bottom)

def display(keypad_with_borders,rowsize):
	for i in range(0,len(keypad_with_borders),rowsize):
		print(keypad_with_borders[i:i+7])

def move_toward(move_seq,keypad_with_borders,border='|'):
	start = cur_pos = len(keypad_with_borders)//2
	print(start)
	borders_ix = (list(range(5)) + 
		list(range(len(keypad_with_borders)-5,len(keypad_with_borders))))
	pins = []
	for row_move in move_seq.split('\n'):
		# print(row_move)
		for move in row_move:
			# print(keypad_with_borders[cur_pos],cur_pos)
			m = DIRS.get(move)
			if move in 'LR':
				if m < 0:
					for i in range(abs(m)):
						if keypad_with_borders[cur_pos - 1] != border:
							cur_pos -= 1
							# print(cur_pos)
				if m > 0:
					for i in range(abs(m)):
						if keypad_with_borders[cur_pos + 1] != border:
							cur_pos += 1
			if move in 'UD':
				if m < 0:
					if cur_pos + m not in borders_ix:
						cur_pos += m
				if m > 0:
					if cur_pos + m not in borders_ix:
						cur_pos += m
		pins.append(keypad_with_borders[cur_pos])
	return pins

# print(move_toward(MOVES,add_borders_to(KEYPAD)))


#################Part 2#####################
diamond = """
    1
  2 3 4
5 6 7 8 9
  A B C
    D
""".strip()

def add_border_to_diamond(diamond):
	data = [''.join(row.split())for row in diamond.split('\n')]
	mid_index = len(data)//2
	filled_diamond = []
	for i,row in enumerate(data):
		left_fill = right_fill = abs(mid_index-i)*'#'
		filled_diamond.append(left_fill+row+right_fill)
	diamond_top = diamond_bottom = '#'*7
	diamond = ['#' + row + '#' for row in filled_diamond]
	return diamond_top + ''.join(diamond) + diamond_bottom

def move_toward_2(move_seq,keypad_with_borders,border='|'):
	start = cur_pos = keypad_with_borders.index('5')
	borders_ix = [i for i,b in enumerate(keypad_with_borders) if b == '#']
	pins = []
	for row_move in move_seq.split('\n'):
		# print(row_move)
		for move in row_move:
			# print(move)
			# print(keypad_with_borders[cur_pos],cur_pos)
			m = DIRS_DIAMOND.get(move)
			if move in 'LR':
				if m < 0:
					for i in range(abs(m)):
						if keypad_with_borders[cur_pos - 1] != border:
							cur_pos -= 1
							# print(cur_pos)
				if m > 0:
					for i in range(abs(m)):
						if keypad_with_borders[cur_pos + 1] != border:
							cur_pos += 1
			if move in 'UD':
				if m < 0:
					if cur_pos + m not in borders_ix:
						cur_pos += m
				if m > 0:
					if cur_pos + m not in borders_ix:
						cur_pos += m
		pins.append(keypad_with_borders[cur_pos])
	return pins
test = """ULL
RRDDD
LURDL
UUUUD""".strip()
print(move_toward_2(MOVES,add_border_to_diamond(diamond),border='#'))
# print(display(add_border_to_diamond(diamond),7))

