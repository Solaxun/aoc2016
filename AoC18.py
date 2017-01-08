row = '..^^.'
row2 = '.^^.^.^^^^'
puzzlecode = '.^^^^^.^^^..^^^^^...^.^..^^^.^^....^.^...^^^...^^^^..^...^...^^.^.^.......^..^^...^.^.^^..^^^^^...^.'
from functools import reduce

def buildrow(row):
    row = '.'+row+'.'
    nextrow = []
    for i in range(len(row)-3 + 1):
        if istrap(row[i:i+3]):
            nextrow.append('^')
        else:
            nextrow.append('.')
    return ''.join(nextrow)

def istrap(section):
    left,center,right = section
    if left == '^' and center == '^' and right == '.':
        return True
    elif center == '^' and right == '^' and left == '.':
        return True
    elif left == '^' and right == '.' and center == '.':
        return True
    elif right == '^' and left == '.' and center == '.':
        return True
    else:
        return False

def build_grid(startrow,numrows):
    startgrid = [[startrow]]
    for i in range(numrows):
        startgrid.append([buildrow(startgrid[i][0])])
    return [row[0] for row in startgrid]

def printgrid(grid):
    for i,row in enumerate(grid):
        print(i,row)

def countsafe(grid):
    return sum(map(lambda x: x.count('.'),grid))

print(countsafe(build_grid(puzzlecode,400000-1)))

