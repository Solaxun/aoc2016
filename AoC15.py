DISKS = """Disc #1 has 13 positions; at time=0, it is at position 1.
Disc #2 has 19 positions; at time=0, it is at position 10.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 7 positions; at time=0, it is at position 1.
Disc #5 has 5 positions; at time=0, it is at position 3.
Disc #6 has 17 positions; at time=0, it is at position 5."""

DISKS2 = """Disc #1 has 13 positions; at time=0, it is at position 1.
Disc #2 has 19 positions; at time=0, it is at position 10.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 7 positions; at time=0, it is at position 1.
Disc #5 has 5 positions; at time=0, it is at position 3.
Disc #6 has 17 positions; at time=0, it is at position 5.
Disc #7 has 11 positions; at time=1, it is at position 0."""

ADDED_DISK = 'Disc #7 has 11 positions; at time=0, it is at position 0.'

import re
from collections import deque

def get_disk_info(disk):
    positions = re.search('(\d+)\spositions',disk).group(1)
    current_position = re.search('position\s(\d+)',disk).group(1)
    return list(map(int,[positions,current_position]))

def setup_disk(disk):
    positions,current_position = get_disk_info(disk)
    disk = deque(range(positions))
    while disk[0] != current_position:
        disk.rotate()
    return disk

def game(disks,time=0):
    disks = [setup_disk(disk)for disk in DISKS.split('\n')]
    rotations = -1-time
    for disk in disks:
        disk.rotate(rotations)
        rotations -= 1
    return disks

def allzero(disks):
    return all([disk[0] == 0 for disk in disks])

time = 0
while True:
    disks = game(DISKS,time)
    if allzero(disks):
        break
    time += 1

print(time)

