'''

Advent of Code - 2018

--- Day 13: Mine Cart Madness ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

from collections import defaultdict

# The tracks are represented as a grid with (0,0) as the coordinates of the top
# left corner.  moving the cart in the diferent directions corresponds to 
# updating its current coordinates as follows:
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

# map input and cart directions
directions = {'^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT}

# calculate new cart direction based on current direction and piece of track
new_direction = {
        #(current_dir, 'track_piece', 'last_turn')
        (UP, '|',  ''): UP,
        (UP, '\\', ''): LEFT,
        (UP, '/',  ''): RIGHT,
        (UP, '+',  0): LEFT, #on intersection direction depends on next turn
        (UP, '+',  1): UP,
        (UP, '+',  2): RIGHT,
        
        (LEFT, '-',  ''): LEFT,
        (LEFT, '\\', ''): UP,
        (LEFT, '/',  ''): DOWN,
        (LEFT, '+',  0): DOWN,
        (LEFT, '+',  1): LEFT,
        (LEFT, '+',  2): UP,

        (RIGHT, '-',  ''): RIGHT,
        (RIGHT, '\\', ''): DOWN,
        (RIGHT, '/',  ''): UP,
        (RIGHT, '+',  0): UP,
        (RIGHT, '+',  1): RIGHT,
        (RIGHT, '+',  2): DOWN,

        (DOWN, '|',  ''): DOWN,
        (DOWN, '\\', ''): RIGHT,
        (DOWN, '/',  ''): LEFT,
        (DOWN, '+',  0): RIGHT,
        (DOWN, '+',  1): DOWN,
        (DOWN, '+',  2): LEFT
        }

class Cart:
    def __init__(self, p, d):
        self.position = p
        self.direction = d
        self.next_turn = 0 # 0 -> left, 1 -> straight, 2 -> right
        self.crashed = False

    def tick_update(self, tracks):
        #take one step in the current direction
        self.position = (self.position[0] + self.direction[0], 
                         self.position[1] + self.direction[1])

        #retrieve the new position on the tracks
        part = tracks[self.position]

        # calculate the new cart direction based on the piece of track and 
        # current direction and last turn
        if part in '\\/|-': #turn left or right depending on current direction
            self.direction = new_direction[(self.direction, part, '')]

        elif part == '+':  #intersection: new direction depends on last turn
            self.direction = new_direction[self.direction, part, self.next_turn]
            self.next_turn = (self.next_turn + 1) % 3

    def crash(self, other):
        return self != other and self.position == other.position

def setup(initial_state):
    '''parse the input and store tracks and carts location'''
    tracks = defaultdict(lambda : "")
    carts = []
    for y, line in enumerate(initial_state):
        for x, p in enumerate(line):
            if p in '^v<>':
                carts.append(Cart((x, y), directions[p]))
                #if its a cart, decode what is the piece of track underneath it
                #based on the cart direction
                tracks[(x, y)] = {'<': '-', '>': '-', '^': '|', 'v': '|'}[p]
            else:
                tracks[(x, y)] = p

    return carts, tracks

def show(tracks, carts):
    '''display a representation of the tracks'''
    (mx, my) = max((k[0], k[1]) for k in tracks.keys())
    for y in range(my + 1):
        r = ""
        for x in range(mx + 1):
            if (x, y) in [c.position for c in carts]:
                r = r + "X"
            else:
                r = r + tracks[(x, y)]
        print(r)

def part1(file_input):
    carts, tracks = setup(file_input)

    while True:
        #ensure that we "move" the carts in the correct order starting with the 
        #for the top to bottom, left to right
        for c in sorted(carts, key=lambda x: (x.position[1], x.position[0])):
            c.tick_update(tracks)

            for other in carts:
                if c.crash(other):
                    #set both carts as crashed
                    c.crashed = other.crashed = True
                    #show(tracks, carts)
                    return c.position
        
def part2(file_input):
    carts, tracks = setup(file_input)

    while True:
        #ensure that we "move" the carts in the correct order starting with the 
        #for the top to bottom, left to right
        for c in sorted(carts, key=lambda x: (x.position[1], x.position[0])):
            c.tick_update(tracks)

            for other in carts:
                if c.crash(other):
                    #set both carts as crashed
                    c.crashed = other.crashed = True
        
        #remove all the carts that have crashed in this tick
        carts = [x for x in carts if x.crashed == False]

        if len(carts) == 1: #only one cart left
            return carts[0].position
            
if __name__=='__main__':
    with open('../input/d13.txt', 'r') as f:
        _input = f.read().splitlines()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))


