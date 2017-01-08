#part1
text = open('./../decodeme.txt').read().split()
transpose = list(zip(*text))
decoded = [[(row.count(letter),letter) for letter in row] for row in transpose]
test = [max(each,key=lambda x:x[0]) for each in decoded]
print(test)


"""
of course, that would be the message - if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data, but for each character, 
the character they actually want to send is slightly less likely than the others. Even after signal-jamming noise, 
you can look at the letter distributions in each column and choose the least common letter to reconstruct the original message.
In the above example, the least common character in the first column is a; in the second, d, and so on. Repeating this process for 
the remaining characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is trying to send?
"""
#part2
text = open('./../decodeme.txt').read().split()
transpose = list(zip(*text))
decoded = [[(row.count(letter),letter) for letter in row] for row in transpose]
test = [min(each,key=lambda x:x[0]) for each in decoded]
print(test)

