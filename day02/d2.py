'''

Advent of Code - 2018

--- Day 2: Inventory Management System ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''
__version__ = '0.1'

import os
from itertools import groupby

def part1(boxIDs):
    twoOfAnyLetter = 0
    hasTwo = False
    threeOfAnyLetter = 0
    hasThree = False

    for boxID in boxIDs:
        for g in [list(g) for k, g in groupby(sorted(boxID))]:
            if len(g) == 2 and hasTwo == False:
                twoOfAnyLetter += 1
                hasTwo = True
            else:
                if len(g) == 3 and hasThree == False:
                    threeOfAnyLetter += 1
                    hasThree = True

        hasTwo = False
        hasThree = False

    return twoOfAnyLetter * threeOfAnyLetter

def part2(boxIDs):
    for boxID1 in boxIDs:
        for boxID2 in boxIDs:
            if len([i for i in range(len(boxID1)) if boxID1[i] != boxID2[i]]) == 1:
                ans = []
                for i in range(len(boxID1)):
                    if boxID1[i] == boxID2[i]:
                        ans.append(boxID1[i])
                return "".join(ans)

if __name__ == '__main__':
    with open('../input/d2.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
