from collections import deque

def part1(elves):
    elves = deque(range(1,elves+1))
    while len(elves) > 1:
        elves.remove(elves[1])
        elves.rotate(-1)
    print(elves)

def part2(elves):
    elves = deque(range(1,elves+1))
    while len(elves) > 1:
        mid = len(elves) // 2
        elves.rotate(-mid)
        elves.popleft()
        elves.rotate(mid-1)
    print(elves)

# part1(3001330)
part2(3001330)

# def elves_faster(elves)
#     elves_set = {i for i in range(1,elves+1)}
#     num = elves
#     cur_elf = 1
#     while num > 1:
#         #elf to kill is in terms of position away from current, so index
#         if num <=3:
#             elf_to_kill = cur_elf + 1
#         else:
#             elf_to_kill = cur_elf + num // 2
#         #so here removing number when should be index, but index is not fast
#         #most likely.. so need to somehow get next number based on index or other way
#         elves_set.remove(elf_to_kill)
#         num -= 1
#         cur_elf += 1