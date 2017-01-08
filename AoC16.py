"""Call the data you have at this point "a".
Make a copy of "a"; call this copy "b".
Reverse the order of the characters in "b".
In "b", replace all instances of 0 with 1 and all 1s with 0.
The resulting data is "a", then a single 0, then "b".
"""

def sequence(a):
    b = ''.join(list(reversed(a)))
    temp = []
    for char in b:
        if char == '1':
            temp.append('0')
        elif char == '0':
            temp.append('1')
        else:
            temp.append(char)
    return a + '0' + ''.join(temp)

def filldisk(disksize,data):
    cursize = int(sequence(data))
    while len(str(cursize)) < disksize:
        cursize = sequence(str(cursize))
    return checksum(str(cursize)[0:disksize])

def checksum(data):
    def checksum_inner(data):
        pairs = list(zip(data[0::2],data[1::2]))
        csum =  ''.join(['1' if p0==p1 else '0' for p0,p1 in pairs])
        return csum
    res = checksum_inner(data)
    while len(res) % 2 == 0:
        res = checksum_inner(res)
    return res
    
print(filldisk(35651584,'10010000000110000'))

