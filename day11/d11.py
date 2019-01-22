'''

Advent of Code - 2018

--- Day 11: Chronal Charge ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict
from itertools import product

def power_level(x, y, serial_number):
    rack_id = x + 10
    power_level = (rack_id * y + serial_number) * rack_id
    return ((power_level // 100) % 10) - 5

def square_power(grid, x, y, size):
    '''returns the sum of the cells in the square with top left corner (x,y)
    and width/height equal to size

    https://en.wikipedia.org/wiki/Summed-area_table#The_algorithm'''
    x0, y0, x1, y1 = x - 1, y - 1, x + size - 1, y + size - 1
    return grid[x0, y0] + grid[x1, y1] - grid[x1, y0] - grid[x0, y1]

def summed_area_table(dimension, serial_num):
    '''https://en.wikipedia.org/wiki/Summed-area_table#The_algorithm'''
    I = defaultdict(int)
    for x, y in product(range(1, dimension+1), range(1, dimension+1)):
        I[x, y] = power_level(x, y, serial_num) + I[x, y-1] + I[x-1, y] - I[x-1, y-1]

    return I

def part1(dimension=300, size=3, serial_number=7803):
    I = summed_area_table(dimension, serial_number)

    max_power = -1e9 
    coords = (0, 0)
    for x, y in product(range(1, dimension+1-size), range(1, dimension+1-size)):
        power = square_power(I, x, y, size)
        if power > max_power:
            max_power = power
            coords = (x, y)

    return max_power, coords, size

def part2():
    return max((part1(300, size, 7803) for size in range(1, 301)), key = lambda
            f : f[0])

if __name__ == '__main__':
    print('Part One: {}'.format(part1()))
    print('Part Two: {}'.format(part2()))

