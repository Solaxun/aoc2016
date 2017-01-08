"""The first floor contains a polonium generator, a thulium generator, 
a thulium-compatible microchip, a promethium generator, 
a ruthenium generator, a ruthenium-compatible microchip, 
a cobalt generator, and a cobalt-compatible microchip.

The second floor contains a polonium-compatible microchip and a
promethium-compatible microchip.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant."""
import itertools
from copy import deepcopy
from heapq import heappop,heappush
import math

state1 = frozenset([('F4',frozenset()),
                    ('F3',frozenset()),
                    ('F2',frozenset(['pM','PM'])),
                    ('F1',frozenset(['EE', 'pG', 'TG', 'TM', 'PG', 'RG', 'RM', 'CG', 'CM']))])

state2 = frozenset([('F4',frozenset()),
                    ('F3',frozenset()),
                    ('F2',frozenset(['pM','PM'])),
                    ('F1',frozenset(['EE', 'pG', 'TG', 'TM', 'PG', 'RG', 'RM', 'CG', 'CM',
                                     'EG','EM','DG','DM']))])

norvig_state = frozenset([('F4',frozenset()),
                          ('F3',frozenset(['pM', 'pG', 'RM', 'RG'])),
                          ('F2',frozenset(['SM','PM'])),
                          ('F1',frozenset(['EE', 'TG', 'TM', 'PG', 'SG']))])#31

smallstate = frozenset([('F4',frozenset()),
                        ('F3',frozenset(['LG'])),
                        ('F2',frozenset(['HG'])),
                        ('F1',frozenset(['EE','HM','LM']))])  

easy = frozenset([('F4',frozenset()),
                  ('F3',frozenset(['RM'])),
                  ('F2',frozenset()),
                  ('F1',frozenset(['EE','RG']))])  

def bfs_paths(state, start, goal,successors):
    queue = [(state, [start])]
    explored = set()
    while queue:
        (state, path) = queue.pop(0)
        if state not in explored:
            explored.add(state)
            for state,action in successors(state).items():
                if isgoal(state):
                    return path + [action]
                else:
                    queue.append((state, path + [action]))

def astar(startstate,goal,successors,heuristic):
    frontier = [(0,startstate)]
    parentmap = {startstate:None}
    existing_costs = {startstate:0}
    while frontier:
        fcost,state = heappop(frontier)
        if isgoal(state): return construct_path(state,startstate,parentmap)
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
    state = dict([(k,list(v)) for k,v in state])
    # total_items = len([el for lst in state.values() for el in lst])
    dist = sum([len(items) * int(floor[1]) for floor,items in state.items()])
    return dist

def isgoal(state):
    state = dict([(k,list(v)) for k,v in state])
    total_items = len([el for lst in state.values() for el in lst])
    return True if len(set(state['F4'])) == total_items else False

def elevator_location(state):
    for floor,items in state.items():
        if 'EE' in items:
            return floor

def neighbor_floors(floor):
    floornum = int(floor[1])
    if floornum == 1:
        return ['F'+ str(floornum+1)]
    elif floornum == 4:
        return ['F'+ str(floornum-1)]
    else:
        return ['F'+str(floornum+1),'F'+str(floornum-1)]

def successors(state):
    state = {floor:list(items) for floor,items in state}
    curfloor = elevator_location(state)
    items = state[curfloor]
    items_to_move = valid_pairs(items)
    # print(items_to_move)
    neighbors = neighbor_floors(curfloor)
    succ = {}
    for item in items_to_move: #tup or single chip
        for nfloor in neighbors:
            #move item from cur floor to neighbor floor if no conflict, that is a new state with
            #item removed from cur floor, add to neighbor floor, do same for elevator
            if no_conflict(item,state[nfloor]):
                new_state = update_state(state,curfloor,item,nfloor)
                hashable_ns = frozenset([(k,frozenset(v)) for k,v in new_state.items()])
                succ[hashable_ns] = '{} items: {} -> {}'.format(curfloor,item,nfloor)
    return succ

def update_state(state,curfloor,item,nfloor):
    newstate = {}
    if isinstance(item,str): item = item, #force single element (strings) to tuple so that calling list() doesn't split items (TG -> T,G)
    new_curfloor = list(filter(lambda x: x not in list(item)+['EE'],
        state[curfloor]))
    new_neighborfloor = ['EE'] + state[nfloor] + list(item)
    for floor,stuff in state.items():
        if floor == curfloor:
            newstate[floor] = new_curfloor
        elif floor == nfloor:
            newstate[floor] = new_neighborfloor
        else:
            newstate[floor] = stuff 
    return newstate

def valid_pairs(items):
    pairs = list(itertools.combinations(filter(lambda x: x != 'EE',items),2))
    valid = []
    for x,y in pairs:
        if x[1] == 'G' and y[1] == 'M' or y[1] == 'G' and x[1] == 'M':
            if x[0] == y[0]:
                valid.append((x,y))
        else:
            valid.append((x,y))
    single_chips = list(filter(lambda x: x.endswith('M'),items))
    single_gen = list(filter(lambda x: x.endswith('G'),items))
    return valid + single_chips + single_gen

def no_conflict(items_moving,neighboritems):
    #items can be neutral pair, two chips, or one chip
    #floor might have gens, no gens, no items
    if isinstance(items_moving,str): items_moving = items_moving,
    combined_floor = list(items_moving) + neighboritems
    gen_in_floor = any(filter(lambda x: x.endswith('G'),combined_floor))
    if gen_in_floor:
        chips = filter(lambda x: x.endswith('M'),combined_floor)
        return all(c[0] + 'G' in combined_floor for c in chips)
    return True

# path = bfs_paths(state2,'F1',isgoal,successors)
# print(len(path)-1)
# import cProfile
# cProfile.run('astar(state1, isgoal, successors, distance)')
path = astar(state1, isgoal, successors, distance)
print(len(path)-1)