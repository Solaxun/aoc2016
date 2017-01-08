
codes = open('AoC4.txt').read().split()
# print(codes)

def process_string(room):
    splittext = room.split('-')
    sector_id = int(splittext[-1][0:3])
    # print(sector_id)
    encrypted = splittext[0:-1]
    checksum = splittext[-1][4:-1]
    encrypted = sorted(''.join([letter for part in encrypted for letter in part]))
    counts = set((list(map(lambda x :(x,encrypted.count(x)) ,encrypted))))
    ordered = sorted(counts,key=lambda x:(x[1],- ord(x[0])),reverse=True)
    res = ''.join([each[0]for each in ordered[0:5]])
    # print(res)
    # print(checksum)
    return sector_id if res == checksum else 0

# print(sum(map(process_string,codes)))

alpha = 'abcdefghijklmnopqrstuvwxyz'

def rotate(word,rotations):
    return ''.join([alpha[(alpha.index(letter)+rotations)%26]
     for letter in word])

test = 'qzmt-zixmtkozy-ivhz-343[abdee]'
def cipher(code):
    temp = code.split('-')
    cipher = temp[0:-1]
    sector_id = int(temp[-1][0:3])
    rotated_cipher = list(map(lambda x:rotate(x,sector_id),cipher))
    return ' '.join(rotated_cipher)


for code in codes:
    decoded = cipher(code)
    if 'northpole' in decoded:
        print(code)

