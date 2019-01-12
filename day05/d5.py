'''

Advent of Code - 2018

--- Day 5: Alchemical Reduction ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

def react(unit1, unit2):
    return abs(ord(unit1) - ord(unit2)) == 32

def react_polymer(polymer):
    res = []
    res.append(polymer[0])

    for p in polymer[1:]:
        if len(res) > 0 and react(p, res[-1]):
            res.pop()
        else:
            res.append(p)

    return len(res)

def part1(polymer):
    return react_polymer(polymer)
    
def part2(polymer):
    units = set([u.lower() for u in polymer])

    return min([react_polymer(polymer.replace(u, '').replace(u.upper(), ''))
        for u in units])

if __name__ == '__main__':
    with open('../input/d05.txt', mode='r') as f:
        _input = f.read()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
