'''

Advent of Code - 2018

--- Day 22: Mode Maze ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict
from itertools import product
import networkx

def erosion_level(geological_index, depth):
    return (geological_index + depth) % 20183 

def region_type(region, cave):
    return {0: ('.', 0), 
            1: ('=', 1),
            2: ('|', 2)}[cave[region[0], region[1]] % 3]

def region_type_(region, cave):
    return [('.', 0), ('=', 1), ('|', 2)][cave[region[0], region[1]] % 3]

def setup_cave(depth, mouth, target):
    gindex = defaultdict(int)
    elevel = defaultdict(int)
    cave = defaultdict(tuple)

    for x, y in product(range(mouth[0], target[0]+1), range(mouth[1],
        target[1]+1)):
        if (x, y) in [mouth, target]:
            gindex[x, y] = 0
        elif x == 0:
            gindex[x, y] = y * 48271
        elif y == 0:
            gindex[x, y] = x * 16807
        else:
            gindex[x, y] = elevel[x-1, y] * elevel[x, y-1]

        elevel[x, y] = erosion_level(gindex[x, y], depth)
        cave[x, y] = region_type((x, y), elevel)

    return cave

def display_cave(mouth, target, cave):
    for y in range(mouth[1], target[1] + 1):
        r = []
        for x in range(mouth[0], target[0] + 1):
            if (x, y) == mouth:
                r.append('M')
            elif (x, y) == target:
                r.append('T')
            else:
                r.append(cave[x, y][0])

        print(''.join(r))

def part1(depth=3339, mouth=(0, 0), target=(10, 715)):
    cave = setup_cave(depth, mouth, target)
    #display_cave(mouth, target, cave)
    
    return sum(v[1] for r, v in cave.items() if mouth[0] <= r[0] <= target[0]
            and mouth[1] <= r[1] <= target[1])
    
def adjacent_regions(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] 

def part2(depth=3339, mouth=(0, 0), target=(10, 715)):
    ROCKY, WET, NARROW = '.=|'
    TORCH, CLIMBING_GEAR, NEITHER = 'TCN'

    valid_tools = {
        ROCKY:  [CLIMBING_GEAR, TORCH],         #rocky
        WET:    [CLIMBING_GEAR, NEITHER],       #wet
        NARROW: [TORCH, NEITHER]}               #narrow

    cave = setup_cave(depth, mouth, (target[0]+50, target[1]+50)) #50 unit buffer

    G = networkx.DiGraph()
    for x, y in product(range(target[0]+50), range(target[1]+50)):
        #swapping tools
        tools = valid_tools[cave[x, y][0]]
        for t1 in tools:
            for t2 in tools:
                if t1 == t2:
                    continue
                G.add_edge((x, y, t1), (x, y, t2), weight=7)

        #move to adjacent region
        for ax, ay in adjacent_regions(x, y):
            if ax < 0 or ax >= target[0]+50:
                continue
            if ay < 0 or ay >= target[1]+50:
                continue

            cur = cave[x, y][0]
            adj = cave[ax, ay][0]

            tools = set(valid_tools[cur]).intersection(valid_tools[adj])
            for t in tools:
                G.add_edge((x, y, t), (ax, ay, t), weight=1)

    shortest_path_len = networkx.dijkstra_path_length(G, (0, 0, TORCH),
           (target[0], target[1], TORCH))

    return shortest_path_len

if __name__=='__main__':
    print('Part One: {}'.format(part1()))
    print('Part Two: {}'.format(part2()))

