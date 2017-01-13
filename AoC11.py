import itertools
from copy import deepcopy
from heapq import heappop,heappush
from collections import deque
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

def bfs_paths(state, start, goal,successors):
    queue = deque([(state, [start])])
    explored = set()
    all_paths = []
    while queue:
        (state, path) = queue.popleft()
        if state not in explored:
            explored.add(state)
            for state,action in successors(state).items():
                if isgoal(state):
                    print('explored: {}'.format(len(explored)))
                    # print(path)
                    # print(state)
                    return path + [action]
                else:
                    queue.append((state, path + [action]))

def construct_path(state,start,parentmap):
    path = [state]
    came_from = parentmap[state]
    while came_from:
        path = path + [came_from]
        came_from = parentmap[came_from]
    return path[::-1]

def distance(state):
    state = dict([(k,list(v)) for k,v in state])
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
    neighbors = neighbor_floors(curfloor)
    succ = {}
    for item in items_to_move: #either a pair or chip alone
        for nfloor in neighbors:
            #move item from cur floor to neighbor floor if no conflict, that is a new state with
            #item removed from cur floor, add to neighbor floor, do same for elevator
            if no_conflict(item,items,state[nfloor]):
                new_state = update_state(state,curfloor,item,nfloor)
                hashable_ns = frozenset([(k,frozenset(v)) for k,v in new_state.items()])
                succ[hashable_ns] = '{} items: {} -> {}'.format(curfloor,item,nfloor)
    return succ

def update_state(state,curfloor,item,nfloor):
    newstate = {}
    #force single element (strings) to tuple so that calling list() doesn't
    #split items (TG -> T,G)
    if isinstance(item,str): item = item, 
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

def no_conflict(items_moving,currentitems,neighboritems):
    #items can be neutral pair, two chips, or one chip
    #floor might have gens, no gens, no items
    if isinstance(items_moving,str): items_moving = items_moving,
    nfloor_items = set(neighboritems) | set(items_moving) 
    oldfloor_items = set(currentitems) - set(items_moving)
    def has_gen(floor):      return any(filter(lambda x: x.endswith('G'),floor))
    def get_chips(floor):    return filter(lambda x: x.endswith('M'),floor)
    def gens_matched(floor): return all(c[0] + 'G' in floor for c in get_chips(floor))
    for f in [nfloor_items,oldfloor_items]:
        if has_gen(f):
            if not gens_matched(f):
                return False
    return True

# import cProfile
# cProfile.run('astar(state1, isgoal, successors, distance)')
path = astar(state2, isgoal, successors, distance)
print(len(path)-1)
# path = bfs_paths(state1,'begin', isgoal, successors) #OBOB, if we exclude start state by subtracting 1, it's one short?
# print(len(path)-1)                                   #fixed next morning: needed to return path + [action] for  bfs, not
#                                                      #just path.  This is bc you checked goal when enqueing, not dequeing.



