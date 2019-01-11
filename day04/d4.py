'''

Advent of Code - 2018

--- Day 4: Repose Record ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import os
from collections import defaultdict
from datetime import datetime
import re

def sleep_pattern(events):
    sleep = defaultdict(lambda: [0 for i in range(60)])

    for event in sorted(events):
        time, action = event[1:].split("] ")
        date = datetime.strptime(time, '%Y-%m-%d %H:%M')

        if "Guard" in action:
            guard = int(re.findall("[\d]+", action)[0])
        elif "asleep" in action:
            start = date.minute
        elif "wakes" in action:
            end = date.minute
            for m in range(start, end):
                sleep[guard][m] += 1

    return sleep

def part1(sleep):
    guard_most_sleep = max(sleep.keys(), key = (lambda g: sum(sleep[g])))
    minute_most_asleep = sleep[guard_most_sleep].index(max(sleep[guard_most_sleep]))
    
    return guard_most_sleep * minute_most_asleep
    
def part2(sleep):
    guard_most_sleep_minute = max(sleep.keys(), key=lambda g: max(sleep[g]))
    minute_most_asleep = sleep[guard_most_sleep_minute].index(max(sleep[guard_most_sleep_minute]))

    return guard_most_sleep_minute * minute_most_asleep

if __name__ == '__main__':
    with open('../input/d04.txt', mode='r') as f:
        _input = f.readlines()

    sleep = sleep_pattern(_input)
    print('Part One: {}'.format(part1(sleep)))
    print('Part Two: {}'.format(part2(sleep)))
