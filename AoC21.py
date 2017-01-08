"""
swap x y index
swap x y actual (even if not in string at least try)
rotate left or right x steps
rotate right based on index of letter x - right once, then right index num plus one more if index >= 4
reverse x through y inclusive (index)
move x to y means remove x, and insert so it ends at pos y
"""

from collections import deque
import re
import itertools

to_scramble = 'abcdefgh'
directions = open('AoC21.txt').read().split('\n')

def swap_index(text,x,y):
    text = [l for l in text]
    text[x],text[y] = text[y],text[x]
    return ''.join(text)

def swap_letter(text,x,y):
    swapped = []
    new_word = []
    for i,letter in enumerate(text):
        if letter == x:
            new_word.append(y)
        elif letter == y:
            new_word.append(x)
        else:
            new_word.append(letter)
    return ''.join(new_word)

def rotate_plain(text,right):
    text = deque(text)
    text.rotate(right)
    return ''.join(text)

def rotate_on_position_letter(text,letter):
    ix = text.index(letter)
    dq = deque(text)
    dq.rotate(1)
    dq.rotate(ix)
    if ix >=4:
        dq.rotate(1)
    return ''.join(dq)

def reverse_through_indexes(text,x,y):
    lower,upper = min(x,y),max(x,y)
    rev = ''.join(list(reversed(text[lower:upper+1])))
    text = text[:lower] + rev + text[upper+1:]
    return text

def move_to(text,x,y):
    text = list(text)
    moveme = text.pop(x)
    text.insert(y,moveme)
    return ''.join(text)

def get_numbers(text):
    return list(map(int,re.findall('\d+',text)))

def parse_inst(inst,salt):
    # print(inst)
    if inst.startswith('rotate right'):
        right = get_numbers(inst)[0]
        return rotate_plain(salt,right)
    if inst.startswith('rotate left'):
        left = get_numbers(inst)[0]
        return rotate_plain(salt,-left)        
    elif inst.startswith('swap position'):
        x,y = get_numbers(inst)
        return swap_index(salt,x,y)      
    elif inst.startswith('reverse positions'):
        x,y = get_numbers(inst)
        return reverse_through_indexes(salt,x,y)
    elif inst.startswith('move position'):
        x,y = get_numbers(inst)
        return move_to(salt,x,y)
    elif inst.startswith('rotate based on'):
        letter = re.findall(r'\b\w\b',inst)[0]
        return rotate_on_position_letter(salt,letter)
    elif inst.startswith('swap letter'):
        left_letter,right_letter = re.findall(r'\b\w\b',inst)
        return swap_letter(salt,left_letter,right_letter)        

def part1(salt):
    for d in directions:
        salt = parse_inst(d,salt) 
    return salt 

def part2(salt):
    for p in itertools.permutations(salt):
        if part1(''.join(p)) == salt:
            return ''.join(p)

# print(part1('abcdefgh'))
print(part2('fbgdceah'))

