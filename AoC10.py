import re
from collections import defaultdict

TEST = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

REAL = open('AoC10.txt').read()

def get_from(instructions,data='bot'):
	return list(filter(
		lambda x: x.startswith(data),instructions.split('\n')))

def get_bot_data(bot):
	botname = re.match('bot \d+',bot).group()
	low_to = re.search('low to (\w+ \d+)',bot).group(1)
	high_to = re.search('high to (\w+ \d+)',bot).group(1)
	return (botname,low_to,high_to)

def get_value_data(val):
	value = re.search('value (\d+)',val).group(1)
	tobot = re.search('bot \d+',val).group()
	return(tobot,value)

def init_bots(instructions):
	bots = get_from(instructions,data='bot')
	botmap = {}
	for bot in bots:
		bot,low_to,high_to = get_bot_data(bot)
		botmap[bot] = {'low':low_to,'high':high_to,'chips':[]}
	return botmap

def target_bot(chips,*target):
	chips = sorted(map(int,chips))
	return True if chips == sorted(target) else False

all_bots = defaultdict(list,init_bots(REAL))
all_values = get_from(REAL,data='value')

def assign_value(bot,value):
	thisbot = all_bots[bot]
	if bot.startswith('output'):
		thisbot.append(value)
	else:
		thisbot['chips'].append(value)
		place_low_in = thisbot['low']
		place_high_in = thisbot['high']
		if len(thisbot['chips']) == 2:
			if target_bot(thisbot['chips'],5,2):
				print('target bot is --> {}'.format(bot))
				# return bot
			assign_value(place_low_in,str(min(thisbot['chips'],key=int)))
			assign_value(place_high_in,str(max(thisbot['chips'],key=int)))
			thisbot['chips'] = []

for value in all_values:
	tobot = get_value_data(value)[0]
	value = get_value_data(value)[1]
	assign_value(tobot,value)

outputs = 1
for bot,val in all_bots.items():
	if re.search('output [012]',bot):
		print(bot,val)
		outputs *= int(val[0])
print(outputs)