import re
from  copy import deepcopy
from heapq import heappush, heappop

PUZZLE = tuple(map(tuple,open('AoC24.txt').read().split('\n')))

def astar(startstate,goal,successors,heuristic):
    frontier = [(0,startstate)]
    parentmap = {startstate:None}
    existing_costs = {startstate:0}
    while frontier:
        fcost,state = heappop(frontier)
        if isgoal(state): 
            print('explored states: {}'.format(len(parentmap)))
            return construct_path(state,startstate,parentmap)
        for newstate,action in successors(state).items():
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
    numlocs = get_num_locs(state)
    x1,y1 = numlocs['0']
    nonzero = {loc for num,loc in numlocs.items() if num != '0'}
    closest_number = min([abs(x1 - x2) + abs(y1 - y2) for x2,y2 in nonzero])
    return closest_number

def get_num_locs(state):
    num_locs = {}
    for i in range(len(state)):
        for j in range(len(state[0])):
            if re.match('\d+',state[i][j]):
                num_locs[state[i][j]] = i,j
    return num_locs

def isgoal(state):
    nonzero = set(get_num_locs(state)) - set('0')
    return not nonzero #no nonzero numbers remaining

def inbounds(x,y,state):
    return 0 <= x < len(state) and 0 <= y < len(state[0]) and state[x][y] != '#'

def successors(state):
    #double check successor func.. make sure states are returned correctly
    #with the zero in the right spot and old spot replaced w/ dot
    state = list(map(list,state))
    succ = {}
    movements = [(0,1),(1,0),(0,-1),(-1,0)]
    number_locations = get_num_locs(state)
    x,y = number_locations['0']
    state[x][y] = '.'
    other_locs = {loc for num,loc in number_locations.items() if num != '0'}
    for m in movements:
        newx,newy = vector_add(m,(x,y))
        if inbounds(newx,newy,state):
            state_copy = deepcopy(state)
            state_copy[newx][newy] = '0'
            succ[tuple(map(tuple,state_copy))] = '{} -> {}'.format((x,y),(newx,newy))
    return succ

def vector_add(x,y):
    return list(map(sum,(zip(x,y))))

print(astar(PUZZLE,isgoal,successors,distance))

