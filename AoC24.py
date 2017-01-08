import re
from  copy import deepcopy
puzzle = list(map(list,open('AoC24.txt').read().split('\n')))

def bfs_paths(state, start, goal,successors):
    queue = [(state, [start])]
    explored = set()
    while queue:
        (state, path) = queue.pop(0)
        state_tup = tuple(map(tuple,state))
        if state_tup not in explored:
            explored.add(state_tup)
            for state,action in successors(state).items():
                if isgoal(state):
                    return path + [action]
                else:
                    queue.append((state, path + [action]))

def get_start(state):
    num_locs = {}
    for i in range(len(state)):
        for j in range(len(state[0])):
            if re.match('\d+',state[i][j]):
                num_locs[state[i][j]] = i,j
    return num_locs

def successors(state):
    succ = {}
    movements = [(0,1),(1,0),(0,-1),(-1,0)]
    number_locations = get_start(state)
    current_loc = number_locations['0']
    state[current_loc[0]][current_loc[1]] = '.'
    other_locs = {loc for num,loc in number_locations.items() if num != 0}
    for m in movements:
        state_copy = deepcopy(state)
        newx,newy = vector_add(m,current_loc)
        try:
            state_copy[newx][newy] = '0'
        except IndexError:
            pass
        succ[tuple(map(tuple,state_copy))] = m
    return succ

def vector_add(x,y):
    return list(map(sum,(zip(x,y))))

