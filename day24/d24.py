'''

Advent of Code - 2018

--- Day 24: Imune System Simulator 20XX ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from enum import Enum, auto
from copy import deepcopy
from itertools import count

class Side(Enum):
    IMMUNE_SYSTEM = auto()
    INFECTION = auto()

class Group:
    def __init__(self, side, units, hp, attack_damage, attack_type, initiative,
            weaknesses=[], immunities=[]):
        self.side = side
        self.units = units
        self.hp = hp
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.boost = 0

        self.target = None
        self.attacker = None

    def reset(self):
        self.target = None
        self.attacker = None

    def effective_power(self):
        return self.units * (self.attack_damage + self.boost)

    def choice_priority(self):
        return (-self.effective_power(), -self.initiative)

    def damage(self, target):
        if target.units == 0:
            return (0, 0, 0)
        if self.attack_type in target.immunities:
            return (0, 0, 0)
        mult = 1
        if self.attack_type in target.weaknesses:
            mult = 2
        return (self.effective_power() * mult, target.effective_power(),
                target.initiative)

    def choose_target(self, candidates):
        cands = [c for c in candidates 
                if c.attacker is None 
                and self.damage(c)[0] > 0]
        if cands:
            self.target = max(cands, key= lambda c: self.damage(c))
            self.target.attacker = self

    def attack(self, target):
        if self.target:
            damage = self.damage(target)[0]
            killed = damage // target.hp
            target.units = max(0, target.units - killed)

class Simulation:
    def __init__(self, groups, boost=0):
        self.groups = groups
        self.boost = boost

    def run(self):
        #apply boost to immune_system if any
        if self.boost:
            for g in self.groups:
                if g.side == Side.IMMUNE_SYSTEM:
                    g.boost = self.boost

        prev = (-1, -1)
        while True:
            #reset target
            for g in self.groups:
                g.reset()

            #target selection
            self.groups = sorted(self.groups, key=lambda g: g.choice_priority())
            for g in self.groups:
                if g.units:
                    g.choose_target([c for c in self.groups if c.side != g.side])

            #attack
            self.groups = sorted(self.groups, key=lambda g: -g.initiative)
            for g in self.groups:
                if g.target and g.target.units:
                    g.attack(g.target)

            immune_system = sum(g.units for g in self.groups if g.side ==
                    Side.IMMUNE_SYSTEM)
            infection = sum(g.units for g in self.groups if g.side ==
                    Side.INFECTION)
            if (immune_system, infection) == prev:
                #detect stalemate
                if immune_system == 0 or infection == 0:
                    return max((infection, 'infection'), (immune_system, 'immune_system'))
                else:
                    return (None, None)
            prev = (immune_system, infection)
    
def parse_input(_input):
    def parse_group(side, line):
        r = re.compile("([0-9]+) units each with ([0-9]+) hit points (\\((.*)\\) |)with an attack that does ([0-9]+) (.*) damage at initiative ([0-9]+)")

        m = re.search(r, line)
        w, i = [], []
        if m.group(4):
            for modifier in m.group(4).split('; '):
                mod, _, args = modifier.split(' ', 2)
                wi = args.split(', ')
                if mod == 'weak':
                    w = wi
                else:
                    i = wi

        return Group(side, int(m.group(1)), int(m.group(2)), int(m.group(5)),
                m.group(6), int(m.group(7)), w, i)

    immune_system_lines = []
    infection_lines = []

    side = Side.IMMUNE_SYSTEM
    for line in _input:
        if line == 'Immune System:':
            side = Side.IMMUNE_SYSTEM
        elif line == 'Infection:':
            side = Side.INFECTION
        elif len(line) > 0:
            if side == Side.IMMUNE_SYSTEM:
                immune_system_lines.append(line)
            else:
                infection_lines.append(line)
    
    immune_system = [parse_group(Side.IMMUNE_SYSTEM, l) for l in immune_system_lines]
    infection = [parse_group(Side.INFECTION, l) for l in infection_lines]

    return immune_system, infection

def part1(_input):
    immune_system, infection = parse_input(_input)

    simulation = Simulation(immune_system + infection)
    (num_units, winning_side) = simulation.run()

    return num_units

def part2(_input):
    immune_system, infection = parse_input(_input)

    for boost in count(1):
        ims = deepcopy(immune_system)
        inf = deepcopy(infection)

        simulation = Simulation(ims + inf, boost)
        (num_units, winning_side) = simulation.run()
        if winning_side == 'immune_system':
            return num_units

if __name__=='__main__':
    with open('../input/d24.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))

