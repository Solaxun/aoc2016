def intialize_puzzle(col,row):
    grid = make_grid(col,row)
    def parse_move(move):
        if move.startswith('rotate column'):
            actions = move.split('rotate column')[1].split('by')
            col = int(actions[0].split('=')[-1])
            rotations = int(actions[1])
            rotate(x=col,rot=rotations,grid=grid)
        elif move.startswith('rotate row'):
            actions = move.split('rotate row')[1].split('by')
            row = int(actions[0].split('=')[-1])
            rotations = int(actions[1])
            rotate(y=row,rot=rotations,grid=grid)
        elif move.startswith('rect'):
            c, r = list(map(int,move.split('rect')[1].split('x')))
            rect(col=c,row=r,grid=grid)
        else: return 'fail'
        print(move)
        print_grid(grid)
        return grid
    return parse_move

def make_grid(col=50,row=6):
    return [['-' for c in range(col)] for r in range(row)]

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def rect(col,row,grid=None):
    for r in range(row):
        for c in range(col):
            grid[r][c] = '#'
    # return grid

def rotate(x=None,y=None,rot=0,grid=None):
    #may need to deal with collisions here.
    #also - if nothing to shift, nothing happens? 
    window = get_row_or_column(grid,column=x,row=y)
    old_pixel_locs = [i for i,pix in enumerate(window) if pix == '#']
    new_pixel_locs = [loc + rot if loc + rot < len(window) 
        else (loc + rot) % len(window) 
        for loc in old_pixel_locs]
    # print(old_pixel_locs,new_pixel_locs)
    updated_window = ['-']*len(window)
    for np_loc in new_pixel_locs:
        updated_window[np_loc] = '#'
    update_grid(grid,updated_window,column=x,row=y)

def update_grid(grid,updated_window,row=None,column=None):
    if column or column == 0:
        for r in range(len(updated_window)):
            grid[r][column] = updated_window[r]
    if row or row == 0:
        for c in range(len(updated_window)):
            grid[row][c] = updated_window[c]
    return grid

def get_row_or_column(grid,row=None,column=None):
    if column or column == 0:
        return [grid[i][column] for i in range(len(grid))]
    if row or row == 0:
        return grid[row]

def count_lights(grid):
    return sum([column == '#' for row in grid for column in row])

# print_grid(parse_move('rect 20x6'))
# test = rect(4,4,make_grid())
# print_grid(test)
# print(get_row_or_column(test,column=3))
# print(rotate(y=3,rot=3,grid=test))

#####update_grid tests###########
# update_grid(test,['#','#','-','-','-','#',],row=None,column=8)
# print()
# print_grid(test)

# update_grid(test,['#']*50,row=2,column=None)
# print()
# print_grid(test)

MOVES = open('AoC8.txt').read().split('\n')
parse_move = intialize_puzzle(col=50,row=6)
for move in MOVES:
    g = parse_move(move)
    print(count_lights(g))
    print()