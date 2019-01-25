'''

Advent of Code - 2018

--- Day 14: Chocolate Charts ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

def part1(target=430971):
    scoreboard = [3, 7]
    elf1 = 0
    elf2 = 1

    while len(scoreboard) < target + 10:
        score = scoreboard[elf1] + scoreboard[elf2]
        scoreboard.extend(divmod(score, 10) if score >= 10 else (score, ))
        elf1 = (elf1 + 1 + scoreboard[elf1]) % len(scoreboard) #1 plus the score of their current recipe
        elf2 = (elf2 + 1 + scoreboard[elf2]) % len(scoreboard) #1 plus the score of their current recipe

    return ''.join(map(str, scoreboard[-10:]))

def part2(target=430971):
    scoreboard = [3, 7]
    elf1 = 0
    elf2 = 1

    digits = list(map(int, str(target)))

    while scoreboard[-len(digits):] != digits and scoreboard[-len(digits)-1:-1] != digits:
        score = scoreboard[elf1] + scoreboard[elf2]
        scoreboard.extend(divmod(score, 10) if score >= 10 else (score, ))
        elf1 = (elf1 + 1 + scoreboard[elf1]) % len(scoreboard) #1 plus the score of their current recipe
        elf2 = (elf2 + 1 + scoreboard[elf2]) % len(scoreboard) #1 plus the score of their current recipe

    return len(scoreboard) - len(digits) - ( 0 if scoreboard[-len(digits)] == digits else 1)

if __name__=='__main__':
    print('Part One: {}'.format(part1()))
    print('Part Two: {}'.format(part2()))


