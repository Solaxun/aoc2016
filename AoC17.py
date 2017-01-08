from hashlib import md5
from operator import add
from copy import deepcopy

MAZE = [['S','d','d','d'],
		['d','d','d','d'],
		['d','d','d','d'],
		['d','d','d','V']] 

BLANK_STATE = [['d','d','d','d'],
			   ['d','d','d','d'],
			   ['d','d','d','d'],
			   ['d','d','d','V']] 

def bfs_paths(state, start, goal,successors):
	queue = [(state, [])]
	explored = set()
	all_paths = []
	while queue:
		(state, path) = queue.pop(0)
		if tuple(path) not in explored:
			explored.add(tuple(path))
			for state,action in successors(state,path).items():
				if isgoal(state):
					all_paths.append(path + [action])
				else:
					queue.append((state, path + [action]))
	return max(all_paths,key=len)

def get_hash(code,path):
	doors = 'UDLR'
	code = code + (''.join(path) or '')
	hashed = md5(code.encode()).hexdigest()[0:4]
	return zip(doors,hashed)

def door_is_open(door):
	return door[1] in 'bcdef'

def cur_loc(state,target):
	for i,row in enumerate(state):
		for j,elem in enumerate(row):
			if elem == target:
				return (i,j)

def successors(state,path):
	move_locs = {'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}
	loc = cur_loc(state,'S')
	moves = [m[0] for m in filter(door_is_open,get_hash('qzthpkfp',path))]
	succ = {}
	for move in moves:
		new_loc = element_add(loc,move_locs[move])
		if valid_move(new_loc,state):
			succ[update_state(deepcopy(BLANK_STATE),new_loc)] = move
	return succ

def isgoal(state):
	return cur_loc(state,'S') == (3,3)

def update_state(clean_state,new_loc):
	row,col = new_loc
	clean_state[row][col] = 'S'
	return tuple(map(tuple,clean_state))

def element_add(*args):
	return list(map(add,*args))

def valid_move(new_loc,state):
	row,col = new_loc
	return (0 <= row < len(state) and
			0 <= col < len(state[0]))

print(len(''.join(bfs_paths(MAZE,'',isgoal,successors))))
