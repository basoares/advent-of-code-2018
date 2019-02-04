'''

Advent of Code - 2018

--- Day 17: Reservoir Research ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from collections import namedtuple

Vein = namedtuple('Vein', ['vertical', 'x', 'y', 'end'])

def parse_vein(vein):
    vertical = vein[0] == 'x'
    a, b = vein.split(', ')
    if vertical:
        x = int(a[2:])
        y, end = [int(i) for i in re.findall(r'\d+', b)]

    else:
        y = int(a[2:])
        x, end = [int(i) for i in re.findall(r'\d+', b)]

    return Vein(vertical, x, y, end)

def parse_scan(scan):
    veins = [parse_vein(s) for s in scan]

    min_x = min(v.x for v in veins) - 1
    max_x = max(v.end if not v.vertical else v.x for v in veins) + 1
    min_y = min(v.y for v in veins)
    max_y = max(v.end if v.vertical else v.y for v in veins) + 1
    
    ground = [['.'] * (max_x - min_x + 1) for _ in range(max_y)]

    for vein in veins:
        if vein.vertical:
            for i in range(vein.y, vein.end + 1):
                ground[i][vein.x-min_x] = '#'
        else:
            for i in range(vein.x, vein.end + 1):
                ground[vein.y][i-min_x] = '#'

    return ground, min_x, max_x, min_y, max_y

def spread_water(ground, origin, min_x, max_x):
    spill = False
    new_sources = []

    #spread left
    (x, y) = origin
    x -= 1
    while x >= min_x:
        g = ground[y][x]
        below = ground[y+1][x]
        if g in '#~':
            x += 1
            break
        
        elif below == '.': #new source
            spill = True
            new_sources.append((x, y))
            break
        elif g == '|' and below == '|':
            break

        x -= 1
    left = x

    #spread right
    (x, y) = origin
    x += 1
    while x <= max_x:
        g = ground[y][x]
        below = ground[y+1][x]
        if g in '#~': 
            x -= 1
            break

        elif below == '.': #new source
            spill = True
            new_sources.append((x, y))
            break

        elif g == '|' and below == '|':
            break

        x += 1
    right = x

    return left, right, spill, new_sources

def source_flow(source, ground, min_x, max_x, max_y):
    (x, y) = source
    start_y = y

    if ground[y][x] == '~':
        return

    y += 1
    while y < max_y and y > start_y:
        g = ground[y][x]

        if g == '.':
            ground[y][x] = '|'
            y += 1
        elif g in '~#':
            y -= 1          #go one level up and check if the water overflows
            left, right, spill, sources = spread_water(ground, (x, y), min_x, max_x)

            for i in range(left, right+1):
                ground[y][i] = '|' if spill else '~' 

            if spill:       #if spill then there is at least one new source
                for s in sources:
                    source_flow(s, ground, min_x, max_x, max_y)

        elif g == '|':  
            return #merge with other sources

def part1(scan, water_spring=(500, 0)):
    ground, min_x, max_x, min_y, max_y = parse_scan(scan)
    ground[water_spring[1]][water_spring[0]-min_x] = '+'

    water_spring = (water_spring[0]-min_x, water_spring[1])
    source_flow(water_spring, ground, 0, max_x-min_x, max_y)

    return sum(1 for x in range(max_x-min_x) for y in range(min_y, max_y) if
            ground[y][x] in '|~')

def part2(scan, water_spring=(500, 0)):
    ground, min_x, max_x, min_y, max_y = parse_scan(scan)
    ground[water_spring[1]][water_spring[0]-min_x] = '+'

    water_spring = (water_spring[0]-min_x, water_spring[1])

    source_flow(water_spring, ground, 0, max_x-min_x, max_y)

    return sum(1 for x in range(max_x-min_x) for y in range(min_y, max_y) if
            ground[y][x] in '~')

if __name__=='__main__':
    with open('../input/d17.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))


