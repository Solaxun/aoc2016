transitions = {'N': {'R':'E',
                     'L':'W'},
               'S': {'R':'W',
                     'L':'E'},
               'E': {'R':'S',
                     'L':'N'},
               'W': {'R':'N',
                     'L':'S'}
              }

MOVES = open('AoC1.txt').read()

def movelist(moves):
    return [move.strip() for move in moves.split(',')]

def walk(movelist):
    facing = 'N'
    compass_moves = {'N':0,'E':0,'S':0,'W':0}
    for move in movelist:
        direction = move[0]
        times = move[1:]
        facing = transitions[facing][direction]
        compass_moves[facing] += int(times)
    return blocks_away(compass_moves)

def blocks_away(compass_moves):
    return (abs(compass_moves['N'] - compass_moves['S'])+
            abs(compass_moves['E'] - compass_moves['W']))

# print(walk(movelist(MOVES)))

##############part2###################

def absmoves(tup): 
    pair = list(map(int,tup))
    return abs(sum(pair))

def sub_moves(move):
    direction, times = move[0], int(move[1:])
    return times * direction

def findloop(movelist):
    facing = 'N'
    cur_pos = (0,0)
    all_submoves = set()
    def update_loc(submoves):
        nonlocal cur_pos
        nonlocal facing
        coord_impact = {'N':(0,-1),'S':(0,1),'E':(1,0),'W':(-1,0)}
        facing = transitions[facing][submoves[0]]
        for sm in submoves:
            moveto = coord_impact[facing]
            cur_pos = tuple(map(sum,zip(moveto,cur_pos)))
            if cur_pos in all_submoves:
                return absmoves(cur_pos)
            else: all_submoves.add(cur_pos)
        # print(cur_pos,submoves)
    for move in movelist:
        dist = update_loc(sub_moves(move))
        if dist:
            return dist
    
all_moves = movelist(MOVES)
# print(findloop(['R3','L2','L2','L5']))
print(findloop(all_moves))


