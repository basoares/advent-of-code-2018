'''

Advent of Code - 2018

--- Day 12: Subterranean Sustainability ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict

def next_generation(state, rules, zero_idx):
    state = list('...' + ''.join(state) + '...')
    zero_idx += 3
    new_state = state[:]
    for p in range(2, len(state) - 2):
        new_state[p] = rules[''.join(state[p-2:p+3])]

    while new_state[0] == '.':
        zero_idx -= 1
        new_state = new_state[1:]
    while new_state[-1] == '.':
        new_state = new_state[:-1]
    
    return new_state, zero_idx

def part1(_input):
    state = _input[0][len('initial state: '):]

    rules = defaultdict(lambda : ".")
    for rule in _input[2:]:
        r, result = rule.split(' => ')
        rules[r] = result

    zero_idx = 0
    for _ in range(20):
        state, zero_idx = next_generation(state, rules, zero_idx)

    return sum(i-zero_idx for i,p in enumerate(state) if p == '#')

def part2(_input):
    state = _input[0][len('initial state: '):]

    rules = defaultdict(lambda : ".")
    for rule in _input[2:]:
        r, result = rule.split(' => ')
        rules[r] = result

    zero_idx = 0
    totals = []
    for i in range(1000):
        state, zero_idx = next_generation(state, rules, zero_idx)
        totals.append(sum(i-zero_idx for i,p in enumerate(state) if p == '#'))

    #Is the difference between the generations constant over time after the 
    #100 generation?
    xdiff =  [totals[n] - totals[n-1] for n in range(1, len(totals))]
    if all([xdiff[100] == xdiff[n] for n in range(100, len(xdiff))]):
        print('Difference is constant: {}'.format(xdiff[100]))
    
    #Visual inspection suggested that every generation after the first 100
    #generations adds 80 to the sum. So I took (50e9 - 1000) * 80 and add
    #that to my program's output to get the answer.
    #print(totals[-1])
    return int((50e9 - 1000) * xdiff[100] + totals[-1])

if __name__ == '__main__':
    with open('../input/d12.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))

