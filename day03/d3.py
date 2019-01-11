'''

Advent of Code - 2018

--- Day No Matter How You Slice It ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import os
from collections import defaultdict
from itertools import product
import re

def parse_claim(claims):
    for claim in claims:
        yield [int(n) for n in re.findall('\d+', claim)]

def part1(claims):
    claimedSquares = defaultdict(int)

    for _, x, y, w, h in parse_claim(claims):
        for xy in product(range(x, x+w), range(y, y+h)):
            claimedSquares[xy] += 1

    return sum(1 for v in claimedSquares.values() if v > 1)

def part2(claims):
    claimedSquares = defaultdict(int)

    for _, x, y, w, h in parse_claim(claims):
        for xy in product(range(x, x+w), range(y, y+h)):
            claimedSquares[xy] += 1

    for claimID, x, y, w, h in parse_claim(claims):
            if all(claimedSquares[xy] == 1 for xy in product(range(x, x+w),
                range(y, y+h))):
                return claimID

if __name__ == '__main__':
    with open('../input/d3.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
