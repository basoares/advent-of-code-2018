'''

Advent of Code - 2018

--- Day 23: Experimental Emergency Teleportation ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
import heapq

def manhattan_distance(a, b):
    '''Manhattan distance between two points on a three dimensional space'''
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def parse_position(position):
    return list(map(int, re.findall(r'-?\d+', position)))

def part1(positions):
    nanobots = [(n[3], tuple(n[:-1])) for n in [parse_position(p) for p in positions]]
    strongest = max(nanobots, key=lambda n: n[0])
    
    return len([x for x in nanobots if manhattan_distance(strongest[1], x[1]) <= strongest[0]])
    
def intersect(box, nanobot):
    d = 0
    for i in (0, 1, 2):
        boxlow, boxhigh = box[0][i], box[1][i] - 1
        d += abs(nanobot[1][i] - boxlow) + abs(nanobot[1][i] - boxhigh)
        d -= boxhigh - boxlow
    d //= 2
    return d <= nanobot[0]

def intersect_count(box, nanobots):
    return sum(1 for n in nanobots if intersect(box, n))

def part2(positions):
    nanobots = [(n[3], tuple(n[:-1])) for n in [parse_position(p) for p in positions]]

    #find a box big enough to contain everything in range
    max_coord = max(max(abs(n[1][i])+n[0] for n in nanobots) for i in (0, 1,
        2))
    box_size = 1
    while box_size <= max_coord:
        box_size *= 2

    initial_box = ((-box_size, -box_size, -box_size), (box_size, box_size,
        box_size))

    workheap =  [(-len(nanobots), -2*box_size, 3*box_size, initial_box)]
    while workheap:
        (negreach, negsz, dist_to_orig, box) = heapq.heappop(workheap)
        if negsz == -1:
            #print("Found closest at %s dist %s (%s bots in range)" %
            #      (str(box[0]), dist_to_orig, -negreach))
            return dist_to_orig
        newsz = negsz // -2
        for octant in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
                   (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
            newbox0 = tuple(box[0][i] + newsz * octant[i] for i in (0, 1, 2))
            newbox1 = tuple(newbox0[i] + newsz for i in (0, 1, 2))
            newbox = (newbox0, newbox1)
            newreach = intersect_count(newbox, nanobots)
            heapq.heappush(workheap,
                       (-newreach, -newsz, manhattan_distance(newbox0, (0, 0, 0)), newbox))

if __name__=='__main__':
    with open('../input/d23.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))

