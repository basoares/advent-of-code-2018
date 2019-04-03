'''

Advent of Code - 2018

--- Day 20: A Regular Map ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict, deque

def parse_routes(regex):
    routes = defaultdict(lambda: 0)
    routes[(0, 0)] = 0
    dist = x = y = 0
    stack = deque([])

    for r in regex[1:-1]:
        if r == '(':
            stack.append((dist, x, y))
        elif r == ')':
            dist, x, y = stack.pop()
        elif r == '|':
            dist, x, y = stack[-1] #peek
        else:
            x += (r == 'E') - (r == 'W')
            y += (r == 'S') - (r == 'N')
            dist += 1
            if (x, y) not in routes or dist < routes[(x, y)]:
                routes[(x, y)] = dist
    return routes

def part1(regex):
    routes = parse_routes(regex)
    return max(routes.values())

def part2(regex):
    routes = parse_routes(regex)
    return sum(1 for r in routes.values() if r >= 1000)

if __name__=='__main__':
    with open('../input/d20.txt', 'r') as f:
        _input = f.readline().strip()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))


