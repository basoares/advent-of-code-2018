'''

Advent of Code - 2018

--- Day 21: Chronal Conversion ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re

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

def parse_program(lines):
    program = []
    ip_register = -1
    for line in lines:
        if '#ip' in line:
            ip_register = int(line[3:])
            continue
        opcode = line.split()[0]
        a, b, c = [int(r) for r in re.findall(r'\d+', line)]
        program.append((opcode, a, b, c))

    return ip_register, program

def part1(lines):
    ip = 0
    registers = [0] * 6

    ip_register, program = parse_program(lines)
    while len(program) > ip >= 0:

        if ip == 28: 
            #if the IF statement in instruction 28 is true the program halts
            #the if is only true if r2 is equal to r0
            #so the answer
            return registers[2]

        #write ip value to ip_register
        registers[ip_register] = ip
        #fetch instruction
        opcode, a, b, c = program[ip]
        #execute instruction
        registers[c] = instructions[opcode](registers, a, b)
        #write ip_register value back to ip 
        ip = registers[ip_register]
        #increment ip
        ip += 1

    return registers

def part2():
    seen = []

    r2 = 0
    while True:             #6 outer loop start
        r5 = r2 | 65536
        r2 = 5234604

        while True:         #8 inner loop start
            r3 = r5 & 255
            r2 += r3
            r2 = r2 & 16777215
            r2 *= 65899 
            r2 = r2 & 16777215	

            if r5 <= 256:
                break
            r5 = int(r5 / 256)
            
        #halt condition
        if r2 in seen:  
            return seen[-1]
        seen.append(r2)

if __name__=='__main__':
    with open('../input/d21.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2()))


