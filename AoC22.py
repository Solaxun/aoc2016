import re
import itertools
from collections import namedtuple,defaultdict
from heapq import heappush,heappop

NODES  = open('AoC22.txt').read().split('\n')[2:]
# NODES = """/dev/grid/node-x0-y0   10T    8T     2T   80%
# /dev/grid/node-x0-y1   11T    6T     5T   54%
# /dev/grid/node-x0-y2   32T   28T     4T   87%
# /dev/grid/node-x1-y0    9T    7T     2T   77%
# /dev/grid/node-x1-y1    8T    0T     8T    0%
# /dev/grid/node-x1-y2   11T    7T     4T   63%
# /dev/grid/node-x2-y0   10T    6T     4T   60%
# /dev/grid/node-x2-y1    9T    8T     1T   88%
# /dev/grid/node-x2-y2    9T    6T     3T   66%""".split('\n')

Node = namedtuple('Node',['x','y','size','used_tb','avail','used_pct','isgoal'])

def make_node(text,goalcoords=(29,0)):#29,0 actual | 2,0 test
	x,y = map(lambda x: int(x[1:]),re.findall('[xy]\d+',text))
	rest = ' '.join(text.split()[1:])
	rest_nums = list(map(int,re.findall('\d+',rest)))
	node = Node(*[x,y]+rest_nums+[True if goalcoords == (x,y) else False])
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

def astar(startstate,goal,successors,heuristic):
	startstate = frozenset(startstate)
	frontier = [(0,startstate)]
	parentmap = {startstate:None}
	existing_costs = {startstate:0}
	while frontier:
		fcost,state = heappop(frontier)
		if isgoal(state): 
			print('explored states: {}'.format(len(parentmap)))
			return construct_path(state,startstate,parentmap)
		for newstate,action in successors(state).items():
			newstate = frozenset(newstate)
			new_gcost = 1 + existing_costs[state]
			if newstate not in parentmap or existing_costs[newstate] > new_gcost:
				heappush(frontier, (heuristic(newstate) + new_gcost, newstate))
				existing_costs[newstate] = new_gcost
				parentmap[newstate] = state
	return 'failure'

def construct_path(state,start,parentmap):
	path = [state]
	came_from = parentmap[state]
	while came_from:
		path = path + [came_from]
		came_from = parentmap[came_from]
	return path[::-1]

def distance(state):
	x,y,*_ = next(filter(lambda x: x.isgoal, state))
	return abs(x - 0) + abs (y - 0)

def isgoal(state):
	# /dev/grid/node-x29-y0    90T   70T    20T   77%
	# /dev/grid/node-x0-y0     85T   64T    21T   75%
	# target_node = [node for node in state if (node.x,node.y) == (2,0)][0] #29
	start_node = [node for node in state if (node.x,node.y) == (0,0)][0]
	return start_node.isgoal
	# return start_node.used_tb == 6 and target_node.used_tb == 0 #64/0

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
	neighborlist[3] += node.used_tb
	nodelist[3] = 0 #index 3 is used
	nodelist[4] += node.used_tb #6 is goal
	if node.isgoal:
		nodelist[6] = False
		neighborlist[6] = True
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

print(len(astar(ALL_NODES,isgoal,successors,distance))-1)

