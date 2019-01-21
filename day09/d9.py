'''

Advent of Code - 2018

--- Day 9: Marble Mania ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from collections import deque, defaultdict

def part1(num_players, last_marble):
    circle = deque([0]) #Put the first marble on the circle
    current_player = 0
    scores = defaultdict(int) #scores[current_player] = score

    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            scores[current_player] += marble
            circle.rotate(7)
            scores[current_player] += circle.popleft()

        else:
            circle.rotate(-2)
            circle.appendleft(marble)
        
        #print('[{}] {}'.format(current_player, circle))
        current_player = marble % num_players 

    return max(scores.values())

if __name__ == '__main__':
    with open('../input/d09.txt', mode='r') as f:
        _input = f.read().strip()

    num_players, last_marble = [int(i) for i in re.findall(r'\d+', _input)]

    #print('Part One: {}'.format(part1(9, 25)))
    print('Part One: {}'.format(part1(num_players, last_marble)))
    last_marble *= 100
    print('Part Two: {}'.format(part1(num_players, last_marble)))

