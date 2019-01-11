'''

Advent of Code - 2018

--- Day 3: No Matter How You Slice It ---

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
    claimed_squares = defaultdict(int)

    for _, x, y, w, h in parse_claim(claims):
        for xy in product(range(x, x+w), range(y, y+h)):
            claimed_squares[xy] += 1

    return sum(1 for v in claimed_squares.values() if v > 1)

def part2(claims):
    claimed_squares = defaultdict(int)

    for _, x, y, w, h in parse_claim(claims):
        for xy in product(range(x, x+w), range(y, y+h)):
            claimed_squares[xy] += 1

    for claim_id, x, y, w, h in parse_claim(claims):
            if all(claimed_squares[xy] == 1 for xy in product(range(x, x+w),
                range(y, y+h))):
                return claim_id

if __name__ == '__main__':
    with open('../input/d03.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
