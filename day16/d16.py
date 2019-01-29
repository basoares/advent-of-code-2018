'''

Advent of Code - 2018

--- Day 16: Chronal Classification ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from collections import defaultdict

instructions = {
    'addr': lambda registers, a, b: registers[a] + registers[b],
    'addi': lambda registers, a, b: registers[a] + b,
    'mulr': lambda registers, a, b: registers[a] * registers[b],
    'muli': lambda registers, a, b: registers[a] * b,
    'banr': lambda registers, a, b: registers[a] & registers[b],
    'bani': lambda registers, a, b: registers[a] & b,
    'borr': lambda registers, a, b: registers[a] | registers[b],
    'bori': lambda registers, a, b: registers[a] | b,
    'setr': lambda registers, a, b: registers[a] ,
    'seti': lambda registers, a, b: a,
    'gtir': lambda registers, a, b: 1 if a > registers[b] else 0,
    'gtri': lambda registers, a, b: 1 if registers[a] > b else 0,
    'gtrr': lambda registers, a, b: 1 if registers[a] > registers[b] else 0,
    'eqir': lambda registers, a, b: 1 if a == registers[b] else 0,
    'eqri': lambda registers, a, b: 1 if registers[a] == b else 0,
    'eqrr': lambda registers, a, b: 1 if registers[a] == registers[b] else 0
    }

def part1(samples):
    behaves_like_three_or_more = 0
    for sample in samples:
        before, op, after = [list(map(int, re.findall(r'-?\d+', s))) for s in
                sample.strip().splitlines()]

        count = 0
        for instr in instructions:
            result = before[:]
            result[op[3]] = instructions[instr](before, op[1], op[2]) 

            if after == result:
                count += 1

        if count >= 3:
            behaves_like_three_or_more += 1

    return behaves_like_three_or_more            

def part2(samples, program):
    candidates = defaultdict(set)

    for sample in samples:
        before, op, after = [list(map(int, re.findall(r'-?\d+', s))) for s in
                sample.strip().splitlines()]

        for instr in instructions:
            result = before[:]
            result[op[3]] = instructions[instr](before, op[1], op[2]) 
            
            #whenever there is a match, "instr" becomes a candidate for op[0]
            if after == result:
                candidates[op[0]].add(instr)
            else:
                #if there is no match, it means that "instr" cannot be a
                #candidate for op[0]
                candidates[op[0]].discard(instr)

    mapping = defaultdict(lambda : "")

    while any(candidates.values()):
        for opcode, instrs in candidates.items():
            if len(instrs) == 1:
                mapping[opcode] = instrs.pop()
                #this (opcode, instr) pair has been precisely determined
                #remove it from all cases where it is ambiguous
                for other in candidates.values():
                    other.discard(mapping[opcode])

    #do we have unique mapping for all opcodes
    assert 16 == len(set(mapping.keys())) == len(set(mapping.values()))

    registers = [0] * 4
    for instr in program.splitlines():
        opcode, a, b, c = [int(i) for i in re.findall(r'-?\d+', instr)]
        registers[c] = instructions[mapping[opcode]](registers, a, b)

    return registers[0]

if __name__=='__main__':
    with open('../input/d16.txt', 'r') as f:
        *samples, _, program = f.read().split('\n\n')

    print('Part One: {}'.format(part1(samples)))
    print('Part Two: {}'.format(part2(samples, program)))


