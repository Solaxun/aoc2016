from copy import deepcopy

DOWN,UP,LEFT,RIGHT = MOVES = [(1,0),(-1,0),(0,-1),(0,1)]

def fillspace(x,y,favnum):
	part1 = x*x + 3*x + 2*x*y + y + y*y
	space = sum(map(int,filter(lambda x: x == '1',get_binary(part1 + favnum))))
	return '.' if space % 2 == 0 else '#'

def get_binary(num):
	return bin(num)[2:]

def gen_grid(x=7,y=10,favnum=1362,start=(1,1)):
	grid =  [[fillspace(c,r,favnum) for c in range(y)] for r in range(x)]
	if start:
		grid[start[0]][start[1]]='O'
	return grid

def print_grid(grid):
	for row in grid:
		print(''.join(row))
	print()

GRID = gen_grid(x=40,y=32)

def bfs_paths(state, start, goal,successors):
	queue = [(state, [start])]
	explored = set()
	while queue:
		(state, path) = queue.pop(0)
		#remove for normal bfs
		if len(path) == 51:
			explored.add(state)
			continue
		state_tup = tuple(map(tuple,state))
		if state_tup not in explored:
			explored.add(state_tup)
			for state,action in successors(state).items():
				curpath = path + [action]
				if goal(state):
					return path + [action]
				queue.append((state, curpath))
	locs = sorted(map(current_position,explored))
	return len(explored)

def current_position(state):
	for i,row in enumerate(state):
		for j,col in enumerate(row):
			if col == 'O': 
				return (i,j)

def isgoal(state):
	return True if current_position(state) == (39,31) else False

def successors(state):
	loc = current_position(state)#get loc then wipe grid
	actions = []
	for m in MOVES:
		actions.append(tuple([loc[0] + m[0], loc[1] + m[1]]))
	succ = {}	
	for row,column in actions:
		statecopy = gen_grid(x=40,y=32,start=False)
		if 0 <= row < len(state) and 0 <= column < len(state[0]):
			if statecopy[row][column] != '#':
				statecopy[row][column] = 'O'
				succ[tuple(map(tuple,statecopy))] = (row,column)
	return succ

#Part 1: minus 1 bc start is on the path, but not an action so remove
# print(len(bfs_paths(GRID,(1,1),isgoal,successors))-1)
#Part 2:
print(bfs_paths(GRID,(1,1),isgoal,successors))
