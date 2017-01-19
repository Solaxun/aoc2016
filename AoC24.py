import re
from  copy import deepcopy
from heapq import heappush, heappop

PUZZLE = tuple(map(tuple,open('AoC24.txt').read().split('\n')))

def astar(startstate,goal,successors,heuristic):
    frontier = [(0,startstate)]
    parentmap = {startstate:None}
    existing_costs = {startstate:0}
    while frontier:
        fcost, state = heappop(frontier)
        if isgoal(state): 
            print('explored states: {}'.format(len(parentmap)))
            return construct_path(state,startstate,parentmap)
        for newstate,action in successors(state).items():
            new_gcost = 1 + existing_costs[state]
            if newstate not in parentmap or existing_costs[newstate] > new_gcost:
                heappush(frontier, (heuristic(newstate) + new_gcost, newstate))
                existing_costs[newstate] = new_gcost
                parentmap[newstate] = state
    return 'failure\nexplored: {}\nfrontier: {}'.format(len(parentmap),frontier)

def construct_path(state,start,parentmap):
    path = [state]
    came_from = parentmap[state]
    while came_from:
        path = path + [came_from]
        came_from = parentmap[came_from]
    return path[::-1]

def distance(state):
    loc, nums_remaining = state
    x1, y1 = loc
    numlocs = get_num_locs(PUZZLE)
    nonzero = {loc for num,loc in numlocs.items() if num in nums_remaining}
    if not nonzero: return 0
    closest_number = min([abs(x1 - x2) + abs(y1 - y2) for x2,y2 in nonzero])
    return closest_number

def get_num_locs(state=PUZZLE):
    num_locs = {}
    for i in range(len(state)):
        for j in range(len(state[0])):
            if re.match('\d+',state[i][j]):
                num_locs[state[i][j]] = i,j
    return num_locs

def isgoal(state):
    _ , nums_to_visit = state
    return not(nums_to_visit)

def inbounds(x,y,state=PUZZLE):
    return 0 <= x < len(state) and 0 <= y < len(state[0]) and state[x][y] != '#'

def successors(state):
    #double check successor func.. make sure states are returned correctly
    #with the zero in the right spot and old spot replaced w/ dot
    cur_loc, nums_to_visit = state
    succ = {}
    movements = [(0,1),(1,0),(0,-1),(-1,0)]
    x,y = cur_loc
    num_locations = get_num_locs(PUZZLE)
    for m in movements:
        newx,newy = vector_add(m,(x,y))
        if inbounds(newx,newy,state=PUZZLE):
            #if newcoords are a nonzero number, remove from numstovisit and update state
            if (newx,newy) in num_locations.values():
                remaining_nums_to_visit = (set(nums_to_visit) - 
                                           set({num for num,loc in num_locations.items()
                                           if loc == (newx,newy)}))
            else:
                remaining_nums_to_visit = nums_to_visit
            state = ((newx,newy),frozenset(remaining_nums_to_visit))
            succ[state] = '{} -> {}'.format((x,y),(newx,newy))
    return succ

def vector_add(x,y):
    return list(map(sum,(zip(x,y))))

numlocs = get_num_locs(PUZZLE)
startloc = numlocs['0']

nums_to_visit = frozenset(set(numlocs) - set('0'))
print(astar((startloc,nums_to_visit),isgoal,successors,distance))
path = astar((startloc,nums_to_visit),isgoal,successors,distance)
for p in path:
    print(p)
print(len(path)-1)
