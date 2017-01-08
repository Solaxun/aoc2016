"""You are faced with a security door designed by Easter Bunny engineers that seem to have acquired most of their 
security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time by finding the MD5 hash of some Door 
ID (your puzzle input) and an increasing integer index (starting with 0).

A hash indicates the next character in the password if its hexadecimal representation starts with five zeroes. If it does, 
the sixth character in the hash is the next character of the password.

For example, if the Door ID is abc:

-The first index which produces a hash that starts with five zeroes is 3231929, which we find by hashing abc3231929; the sixth 
character of the hash, and thus the first character of the password, is 1.

-5017308 produces the next interesting hash, which starts with 000008f82..., so the second character of the password is 8.

-The third time a hash starts with five zeroes is for abc5278568, discovering the character f.
In this example, after continuing this search a total of eight times, the password is 18f47a30.

Given the actual Door ID, what is the password?"""


#ID + increasing integer until starts with 5 zeroes
#sixth char is next char in PW

from hashlib import md5

def get_md5(string):
	return md5(string.encode()).hexdigest()

def generate_candidate(door_id,pos=5):
	start_ix = 0
	while True:
		candidate = get_md5(door_id+str(start_ix))
		start_ix += 1
		if candidate[0:5] == '00000':
			yield candidate[pos]

def get_password(door_id):
	genc = generate_candidate(door_id)
	return ''.join([next(genc) for i in range(8)])

# print(get_password('reyedfim'))

"""
--- Part Two ---

As the door slides open, you are presented with a second door that uses a slightly more inspired security mechanism. 
Clearly unimpressed by the last version (in what movie is the password decrypted in order?!), the Easter Bunny engineers 
have worked out a better solution.

Instead of simply filling in the password from left to right, the hash now also indicates the position within the password to fill. 
You still look for hashes that begin with five zeroes; however, now, the sixth character represents the position (0-7), and the seventh
character is the character to put in that position.

A hash result of 000001f means that f is the second character in the password. Use only the first result for each position, and ignore 
invalid positions.

For example, if the Door ID is abc:

The first interesting hash is from abc3231929, which produces 0000015...; so, 5 goes in position 1: _5______.
In the previous method, 5017308 produced an interesting hash; however, it is ignored, because it specifies an invalid position (8).
The second interesting hash is at index 5357525, which produces 000004e...; so, e goes in position 4: _5__e___.
You almost choke on your popcorn as the final character falls into place, producing the password 05ace8e3.

Given the actual Door ID and this new method, what is the password? Be extra proud of your solution if it uses a cinematic "decrypting" animation.
"""

def get_password_positional(door_id):
	genc = generate_candidate(door_id,pos=slice(5,7))
	slots = [False] * 8
	for ix,val in genc:
		if ix.isalpha(): continue
		ix = int(ix)
		if ix <= len(slots) - 1 and not slots[ix]:
			slots[ix] = val
			if sum(map(bool,slots)) == 8:
				return ''.join(slots)

print(get_password_positional('reyedfim')) 

