'''

Advent of Code - 2018

--- Day 1: Chronal Calibration ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import os
from itertools import cycle

def part1(frequency_changes, current_frequency=0):
    for frq in frequency_changes:
        try:
           chg = int(frq)
           current_frequency += chg
        except ValueError:
            print('{} is not a number!'.format(frq))

    return current_frequency

def part2(frequency_changes, current_frequency=0):
# holds all the frequencies reached 
    frequencies_reached = set()

    for frq in cycle(frequency_changes):
            try:
                chg = int(frq)
                current_frequency += chg
                if current_frequency in frequencies_reached:
                    break;
                else:
                    frequencies_reached.add(current_frequency)
            except ValueError:
                print('{} is not a number'.format(frq))

    return current_frequency



if __name__ == '__main__':
    with open('../input/d01.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
