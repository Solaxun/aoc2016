blacklist = sorted(open('AoC20.txt').read().split('\n'),
    key = lambda x: int(x.split('-')[0]))

cur_max = 0
res = []
for iprange in blacklist:
    left,right = map(int,iprange.split('-'))
    if right > cur_max:
        if left > cur_max+1:
            res.append(cur_max + 1)
        cur_max = right
print(len(res))        
