'''

Advent of Code - 2018

--- Day 1: Chronal Calibration ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import os
from itertools import cycle

def part1(frequencyChanges, currentFrequency=0):
    for frq in frequencyChanges:
        try:
           chg = int(frq)
           currentFrequency += chg
        except ValueError:
            print('{} is not a number!'.format(frq))

    return currentFrequency

def part2(frequencyChanges, currentFrequency=0):
# holds all the frequencies reached 
    frequenciesReached = set()

    for frq in cycle(frequencyChanges):
            try:
                chg = int(frq)
                currentFrequency += chg
                if currentFrequency in frequenciesReached:
                    break;
                else:
                    frequenciesReached.add(currentFrequency)
            except ValueError:
                print('{} is not a number'.format(frq))

    return currentFrequency



if __name__ == '__main__':
    with open('../input/d1.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
