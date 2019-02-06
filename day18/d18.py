'''

Advent of Code - 2018

--- Day 18: Settlers of The North Pole ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict, Counter
from itertools import count, product
import tqdm


def next_minute(lumber_collection, w, h):
    res = defaultdict(lambda : "")

    def adjacent_acres(acre):
        return [lumber_collection[(acre[0]+x, acre[1]+y)] for (x, y) in 
                product((-1, 0, 1), (-1, 0, 1)) if x or y]

    for y in range(h):
        for x in range(w):
            c = lumber_collection[(x, y)]
            counts = Counter(adjacent_acres((x, y)))
            if c == '.':
                if counts['|'] >= 3:
                    c = '|'
            elif c == '|':
                if counts['#'] >= 3:
                    c = '#'
            elif c == '#':
                if counts['#'] < 1 or counts['|'] < 1:
                    c = '.'

            res[(x, y)] = c
    return res

def part1(area, w=50, h=50):
    lumber_collection = defaultdict(lambda: "")
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            lumber_collection[(x, y)] = c

    for i in range(10):
        lumber_collection = next_minute(lumber_collection, w, h)

    #for y in range(h):
    #    r = []
    #    for x in range(w):
    #        r.append(lumber_collection[(x, y)])
    #    print(''.join(r))

    num_trees = sum(1 for v in lumber_collection.values() if v == '|')
    num_lumberyards = sum(1 for v in lumber_collection.values() if v == '#')

    return num_trees * num_lumberyards

def part2(area, w=50, h=50):
    lumber_collection = defaultdict(lambda: "")
    for y, line in enumerate(area):
        for x, c in enumerate(line):
            lumber_collection[(x, y)] = c

    totals = defaultdict(lambda : 0)
    prev = 0
    for i in tqdm.trange(1, 10000):
        lumber_collection = next_minute(lumber_collection, w, h)
        counts = Counter(lumber_collection.values())
        total = counts['|'] * counts['#']
        period = i - totals[total]
        if period == prev:
            if 1000000000 % period == i % period:
                return total
        totals[total] = i
        prev = period

if __name__=='__main__':
    with open('../input/d18.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))


