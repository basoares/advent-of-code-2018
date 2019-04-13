'''

Advent of Code - 2018

--- Day 25: Four-Dimensional Adventure ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
import networkx as nx

def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) + abs(a[3] - b[3])

def part1(coords):
    coordinates = [tuple(map(int, re.findall(r'-?\d+', c))) for c in coords]
    
    neighbours = nx.Graph()
    for c1 in coordinates:
        for c2 in coordinates:
            if manhattan_distance(c1, c2) <= 3:
                neighbours.add_edge(c1, c2)

    return nx.number_connected_components(neighbours)

if __name__ == '__main__':
    with open('../input/d25.txt', mode='r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
