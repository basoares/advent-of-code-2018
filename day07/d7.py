'''

Advent of Code - 2018

--- Day 7: The Sum of Its Parts ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict
from itertools import count
import re

def part1(instructions):
    in_degree = defaultdict(int)
    edges = defaultdict(list)

    for i in instructions:
        match = re.match(r'^Step (.) must be finished before step (.) can '
                'begin.$', i)
        edges[match.group(1)].append(match.group(2))
        in_degree[match.group(2)] += 1

    #Pick all the vertices with in-degree as 0 and add them into a queue
    #If more than one step is ready, choose the step which is first alphabetically
    zero_order = []
    for e in sorted([k for k in edges.keys() if in_degree[k] == 0]):
        zero_order.append(e)

    ans = []
    while zero_order:
        v = zero_order.pop(0)
        ans += v
        for n in edges[v]:
            in_degree[n] -= 1
            if in_degree[n] == 0:
                zero_order.append(n)

        #we need to make sure that vertices with the same order are 
        #sorted alphabetically
        zero_order.sort()
                
    return ''.join(ans)

def step_duration(step):
    return 60 + ord(step) - ord('A') + 1

def part2(instructions, workers=5):
    in_order = defaultdict(int)
    edges = defaultdict(list)
    
    for i in instructions:
        match = re.match(r'Step (.) must be finished before step (.) can '
                 'begin.', i)
        edges[match.group(1)].append(match.group(2))
        in_order[match.group(2)] += 1
        
    ready_steps = []
    for e in sorted([k for k in edges.keys() if in_order[k] == 0]):
        ready_steps.append((e, step_duration(e)))

    #tuple (step, end_time)
    in_progress = []
    
    for seconds_elapsed in count():
        #steps that ended in this iteration                                           
        ended = [s[0] for s in in_progress if s[1] == seconds_elapsed]
        for e in ended:
            workers += 1
            for n in edges[e]:
                in_order[n] -= 1
                #we can release the steps that were dependent on only this step
                if in_order[n] == 0:
                    ready_steps.append((n, seconds_elapsed + step_duration(n)))

                ready_steps.sort(key = lambda t : t[1])

        #remove the steps that ended in this iteration
        in_progress = [step for step in in_progress if step[1] >
                seconds_elapsed]
                                               
        while workers and ready_steps:
            v = ready_steps.pop(0)
            workers -= 1
            in_progress.append((v[0], v[1]))
            
        if not ready_steps and not in_progress:
            return seconds_elapsed 

if __name__ == '__main__':
    with open('../input/d07.txt', mode='r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))
