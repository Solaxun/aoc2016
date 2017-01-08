import re
import itertools
from collections import namedtuple,defaultdict
NODES  = open('AoC22.txt').read().split('\n')[2:]

Node = namedtuple('Node',['x','y','size','used_tb','avail','used_pct'])

def make_node(text):
	x,y = map(lambda x: int(x[1:]),re.findall('[xy]\d+',text))
	rest = ' '.join(text.split()[1:])
	rest_nums = list(map(int,re.findall('\d+',rest)))
	node = Node(*[x,y]+rest_nums)
	return node

ALL_NODES = list(map(make_node,NODES))
ALL_NODE_COMBS = itertools.combinations(ALL_NODES,2)

def part1():
	total_adjacent = 0
	for nodes in ALL_NODE_COMBS:
		left_node,right_node = nodes
		if left_node.used_pct != 0 and left_node.used_tb <= right_node.avail:
			total_adjacent +=1
		elif right_node.used_pct != 0 and right_node.used_tb <= left_node.avail:
			total_adjacent += 1
	return total_adjacent

def bfs_paths(state, start, goal,successors):
	queue = [(state, [start])]
	explored = set()
	while queue:
		(state, path) = queue.pop(0)
		state_tup = frozenset(map(tuple,state))
		if state_tup not in explored:
			explored.add(state_tup)
			for state,action in successors(state).items():
				if isgoal(state):
					return path + [action]
				else:
					queue.append((state, path + [action]))

def isgoal(state):
	# /dev/grid/node-x29-y0    90T   70T    20T   77%
	# /dev/grid/node-x0-y0     85T   64T    21T   75%
	target_node = [node for node in state if (node.x,node.y) == (29,0)][0]
	start_node = [node for node in state if (node.x,node.y) == (0,0)][0]
	return start_node.used_tb == 64 and target_node.used_tb == 0

def successors(state):
	#state is list of nodes
	node_to_neighbors = construct_graph(state)
	#must move all data, so only successors of target capacity < cur used
	succ = {}
	for node in state:
		# print(node)
		node_neighbors = node_to_neighbors[node]
		for neighbor in node_neighbors:
			cur_state = node_map(state) #map from x,y to actual node
			if transferable(node,neighbor):
				# print('node',node.x,node.y,'used',node.used_tb)
				# print('neighbor',neighbor.x,neighbor.y,'avail',neighbor.avail)
				# print()
				new_state = update_state(cur_state,node,neighbor)
				succ[new_state.values()] = str((node.x,node.y)) + '->' + str((neighbor.x,neighbor.y))
	return succ

def update_state(statedict,node,neighbor):
	nodelist = list(node)
	neighborlist = list(neighbor)
	neighborlist[4] -= node.used_tb #index 4 is avail
	nodelist[3] = 0 #index 3 is used
	newnode = Node(*nodelist)
	newneighbor = Node(*neighborlist)
	statedict[newneighbor.x,newneighbor.y] = newneighbor
	statedict[newnode.x,newnode.y] = newnode
	return statedict

def transferable(node,neighbor):
	return neighbor.avail >= node.used_tb and node.used_tb > 0

def neighbors():
	xmax,ymax = get_node_bounds()
	def get_neighbors(node):
		movements = [(0,1),(1,0),(0,-1),(-1,0)]
		x,y = node.x,node.y
		adj = [(x + m[0], y + m[1]) for m in movements]
		not_out_of_bounds = [(x,y) for x,y in adj 
			if 0 <= x <= xmax and  0 <= y <= ymax]       
		return not_out_of_bounds
	return get_neighbors
	
def get_node_bounds(all_nodes=ALL_NODES):
	xmax, ymax = 0, 0
	for n in all_nodes:
		if n.x > xmax:
			xmax = n.x
		if n.y > ymax:
			ymax = n.y
	return xmax,ymax

def node_map(nodes):
	return {(node.x,node.y):node for node in nodes}

def construct_graph(all_nodes=ALL_NODES):
	node_lookup = node_map(all_nodes)
	get_neighbors = neighbors()
	graph = defaultdict(list)
	for node in all_nodes:
		for neighbor in get_neighbors(node):
			graph[node].append(node_lookup[neighbor])
	return graph

print(bfs_paths(ALL_NODES,'',isgoal,successors))
