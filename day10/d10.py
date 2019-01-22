'''

Advent of Code - 2018

--- Day 10: The Stars Align ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from collections import namedtuple
from itertools import count

Light = namedtuple('Light', ['x', 'y', 'vx', 'vy'])

def position(light, s):
    '''Position of light at second s'''
    return Light(light.x + s * light.vx, light.y + s * light.vy, light.vx, light.vy)

def region_size(lights):
    max_x = max(l.x for l in lights)
    min_x = min(l.x for l in lights)
    max_y = max(l.y for l in lights)
    min_y = min(l.y for l in lights)
    return (max_x - min_x) * (max_y - min_y)

def print_sky(lights):
    max_x = max(l.x for l in lights)
    min_x = min(l.x for l in lights)
    max_y = max(l.y for l in lights)
    min_y = min(l.y for l in lights)

    for y in range(min_y - 1, max_y + 2):
        row = []
        for x in range(min_x - 1, max_x + 2):
            if (x, y) in [(l.x, l.y) for l in lights]:
                row.append('#')
            else:
                row.append('.')
        print(''.join(row))

def part1(lights):
    init = []
    for l in lights:
        x, y, vx, vy = [int(i) for i in re.findall(r'-?\d+', l)]
        init.append(Light(x, y, vx, vy))
    
    min_size = float('inf')
    for t in count(0):
        sky = [position(l, t) for l in init]
        #sky = list(map(lambda l: position(l, t), init))
        area = region_size(sky) 
        if area > min_size:
            #print_sky([position(l, t-1) for l in init])
            return ([position(l, t-1) for l in init], t-1)
        else:
            min_size = area
    
if __name__ == '__main__':
    with open('../input/d10.txt', mode='r') as f:
        _input = f.read().splitlines()

    (lights, s) = part1(_input)
    print('Part One:')
    print_sky(lights)
    print('Part Two: {}'.format(s))

