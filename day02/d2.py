'''

Advent of Code - 2018
--- Day 2: Inventory Management System ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import os
from collections import Counter

def part1(box_ids):
    has_two = False
    has_three = False

    for i in box_ids:
        c = Counter(i)
        if len([k for k,v in c.items() if v == 2]) > 0:
            has_two += 1
        if len([k for k,v in c.items() if v == 3]) > 0:
            has_three += 1
            
    return has_two * has_three

def part2(box_ids):
    for box_id1 in box_ids:
        for box_id2 in box_ids:
            if len([i for i in range(len(box_id1)) if box_id1[i] != box_id2[i]]) == 1:
                #print('Candidate boxes: {} and {}'.format(box_id1, box_id2))
                ans = []
                for i in range(len(box_id1)):
                    if box_id1[i] == box_id2[i]:
                        ans.append(box_id1[i])
                return "".join(ans)

if __name__ == '__main__':
    with open('../input/d02.txt', mode='r') as f:
        _input = f.readlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
