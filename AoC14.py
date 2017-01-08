import hashlib
from functools import lru_cache

@lru_cache(maxsize=None)
def md5(text,repeat=2016):
	for i in range(repeat+1):
		text = hashlib.md5(text.encode()).hexdigest().lower()
	return text

def gen_keys(salt):
	num = 0
	keys = 0
	while True:
		trip = find_repeats(md5(salt+str(num)),3)
		if trip:
			for i in range(num+1,num+1001):
				quin = find_repeats(md5(salt+str(i)),5)
				if quin:
					if quin[0:3] == trip:
						keys += 1
						if keys == 64:
							return num
						break
		num += 1

def find_repeats(text,times):
	repeats = [text[i:i+times] for i in range(len(text)-times + 1)]
	for r in repeats:
		if len(set(r)) == 1:
			return r

#22728 abc part 1
#22551 abc part 2
#23769 actual part 1
#      actual part 2
#fails part 2 with stretching but not abc?
test = 'abc'
realvar = 'cuanljph'
print(gen_keys(realvar))
