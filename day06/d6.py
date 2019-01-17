'''

Advent of Code - 2018

--- Day 6: Chronal Coordinates ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict, Counter
from itertools import product, chain

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def closest_coordinate(p, coordinates):
    distance = {}
    for c in coordinates:
        distance[c] = manhattan_distance(p, c)

    c1, c2 = sorted(distance.items(), key = lambda kv: kv[1])[:2]
    #return the coordinate that is closest to p, if there is no tie
    return c1[0] if c1[1] < c2[1] else None

def part1(coordinates):
    min_x = min(coordinates, key = lambda p: p[0])[0]
    max_x = max(coordinates, key = lambda p: p[0])[0]
    min_y = min(coordinates, key = lambda p: p[1])[1]
    max_y = max(coordinates, key = lambda p: p[1])[1]

    grid = product(range(min_x, max_x), range(min_y, max_y))

    area_size = Counter(closest_coordinate(p, coordinates) for p in grid)

    perimeter_box = chain([(min_x, y) for y in range(min_y, max_y)],
                          [(max_x, y) for y in range(min_y, max_y)],
                          [(x, min_y) for x in range(min_x, max_x)],
                          [(x, max_y) for x in range(min_x, max_x)])

    #infinite areas are those that touch the edges of the perimeter box
    infinite_areas = set()
    for p in perimeter_box:
        coord = closest_coordinate(p, coordinates)
        if coord is not None:
            infinite_areas.add(coord)

    return max(size for c, size in area_size.items() if c not in infinite_areas)

def part2(coordinates, max_distance=10000):
    max_x = max(coordinates, key = lambda p: p[0])[0]
    max_y = max(coordinates, key = lambda p: p[1])[1]

    grid = product(range(max_x+1), range(max_y+1))

    region_size = 0
    for p in grid:
        total_distance = sum(manhattan_distance(p, c) for c in coordinates)
        if total_distance < max_distance:
            region_size += 1

    return region_size

if __name__ == '__main__':
    with open('../input/d06.txt', mode='r') as f:
        _input = f.read().splitlines()

    coords = [tuple(map(int, c.split(', '))) for c in _input]

    print('Part One: {}'.format(part1(coords)))
    print('Part Two: {}'.format(part2(coords)))
