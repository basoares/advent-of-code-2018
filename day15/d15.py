'''

Advent of Code - 2018

--- Day 15: Beverage Bandits ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from enum import Enum
from collections import deque
from itertools import count

class Race(Enum):
    elf = 'E'
    goblin = 'G'

class Unit:
    def __init__(self, position, race, attack_power=3, hp=200):
        self.position = position
        self.race = race
        self.hp = hp
        self.attack_power = attack_power if race == Race.elf else 3

class Game:
    def __init__(self, area, elf_attack_power=3):
        self.area = []
        self.walls = set()
        self.units = [] 
        self.rounds = 0

        for y, line in enumerate(area):
            self.area.append(list(line.strip()))
            for x, c in enumerate(line):
                if c == '#':
                    self.walls.add((x, y))
                elif c in 'EG':
                    self.units.append(Unit((x, y), Race(c),
                        attack_power=elf_attack_power))
                    self.area[y][x] = '.'

    def occupied_squares(self):
        '''Coordinates of the walls and the squares occupied by the Elves and Goblins'''
        return self.walls | set([u.position for u in self.units if u.hp > 0])

    def show_area(self):
        print('Status after {} rounds: '.format(self.rounds))
        for y, row in enumerate(self.area):
            r = []
            for x, a in enumerate(row):
                if (x, y) in [u.position for u in self.units]:
                    r.append([u.race.value for u in self.units if u.position == (x,
                        y)][0])
                else:
                    r.append(a)
            scores = ', '.join(f"{u.race.value}({u.hp})" for u in
                               sorted([x for x in self.units
                                       if x.position[1] == y],
                                      key=lambda z: z.position[0]))
            print(''.join(r) + '\t' + scores)

    def turn(self):
        #units take their turns in reading order (top-to-bottom, left-to-right)
        for unit in sorted(self.units, key=lambda u: (u.position[1],
            u.position[0])):

            #units that died during the round
            if unit.hp <= 0:
                continue

            #find the unit's next action: attack or move
            targets, action = self.next_action(unit)    

            #no valid target was found - end game
            if action == 'no_action':
                return False

            if action == 'move' and targets:
                self.move_unit(unit, targets)

                #unit has moved, lets see if it is in range of a target
                targets, action = self.next_action(unit)

            if action == 'attack' and targets:
                #pick the target with fewest hp that is closest in reading order
                t = sorted(targets, key = lambda x : (x.hp, x.position[1],
                             x.position[0]))[0]

                self.attack_target(unit, t)

        #after each turn, remove any units that have died
        self.units = [u for u in self.units if u.hp > 0]

        self.rounds += 1
        #self.show_area()

        return True

    def adjacent_positions(self, position):
        return set([(position[0] + a, position[1] + b) 
            for a, b in [(0, -1), (-1, 0), (1, 0), (0, 1)]])

    def next_action(self, unit):
        '''determines whether a unit should attack or move.
        if the unit is in range of one or more targets, return the target(s)
        and set the action to "attack"
        if it is not in range of a target, return all the targets that have 
        squares in range and set the action to "move"
        if there are not more targets, return "no_action" to end the game
        '''
        #if there are no targets, return "no_action"
        if len([t for t in self.units if t.race != unit.race and t.hp > 0]) == 0:
            return None, 'no_action'

        can_attack = []
        pos = self.adjacent_positions(unit.position)
        can_attack = [t for t in self.units for p in pos if t.race is not
                unit.race and t.hp > 0 and
                t.position[0] == p[0] and t.position[1] == p[1]]
        
        if can_attack:
            return can_attack, 'attack'

        #all squares that are occupied with walls or other units
        occupied = self.occupied_squares()
        #all targets with open adjacent squares
        targets = []
        for t in self.units:
            if t is not unit and t.race is not unit.race and t.hp > 0:
                if self.adjacent_positions(t.position) - occupied:
                    targets.append(t)

        return targets, 'move'

    def move_unit(self, unit, targets):
        '''from the list of targets, move towards the one that is reachable 
        and is closest in reading order
        '''
        results = []
        best = None
        occupied = self.occupied_squares()
       
        in_range = []
        for t in targets:
            in_range.extend(self.adjacent_positions(t.position)-occupied)

        visited = occupied - set([unit.position])
        queue = deque([(0, [unit.position])])
        while queue:
            distance, path = queue.popleft()
            if best and len(path) > best:
                break
            node = path[-1]
            if node in in_range:
                results.append(path)
                best = len(path)
                continue
            if node in visited:
                continue
            visited.add(node)
            for neighbor in sorted(self.adjacent_positions(node), key = lambda
                    x : (x[1], x[0])):
                if neighbor in visited:
                    continue
                queue.append((distance + 1, path + [neighbor]))
        
        if results:
            coordinate = self.best_move(results)
            unit.position = coordinate

    def best_move(self, moves):
        '''Decide which of the paths found should be taken based on the given
        rules'''

        #if there is only one path found, return the first move
        if len(moves) == 1:
            return moves[0][1]

        #create pairs (first_coordinate, final_coordinate)
        paths = [(p[1], p[-1]) for p in moves]
        paths.sort(key = lambda x : (x[1][1], x[1][0], x[0][1], x[0][0]))

        # order the paths by destination and initial coordinate
        # both in reading order
        return paths[0][0]

    def attack_target(self, unit, target):
        target.hp -= unit.attack_power

    def num_elves(self):
        return len([u for u in self.units if u.race is Race.elf and u.hp > 0])

    def run(self):
        while True:
            if not self.turn():
                return self.rounds, self.total_hp(), self.num_elves()

    def total_hp(self):
        return sum(u.hp for u in self.units if u.hp > 0)

def part1(area):
    game = Game(area)
    rounds, total_hp, _ = game.run() 
    game.show_area()

    return rounds * total_hp

def part2(area):
    for p in count(4):
        game = Game(area, elf_attack_power=p)
        num_elves = game.num_elves()
        rounds, total_hp, num_elves_alive = game.run()

        if num_elves == num_elves_alive:
            game.show_area()
            return rounds * total_hp

if __name__=='__main__':
    with open('../input/d15.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))


