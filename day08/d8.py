'''

Advent of Code - 2018

--- Day 8: Memory Maneuver ---

Released under the MIT License <http://opensource.org/licenses/mit-license.php>

'''

import re
from collections import namedtuple

Tree = namedtuple('Tree', ['children', 'metadata'])

def parse_tree(tree_data):
    '''
    A node consists of:
        A header, which is always exactly two numbers:
            The quantity of child nodes.
            The quantity of metadata entries.
        Zero or more child nodes (as specified in the header).
        One or more metadata entries (as specified in the header).
    '''
    child_nodes, metadata_entries = tree_data.pop(0), tree_data.pop(0)

    return Tree([parse_tree(tree_data) for _ in range(child_nodes)],
                [tree_data.pop(0) for _ in range(metadata_entries)])

def sum_metadata(tree):
    return sum(tree.metadata) + sum(map(sum_metadata, tree.children))

def part1(license_file):
    data  = [int(i) for i in re.findall(r'\d+', license_file)]

    root = parse_tree(data) 
    return sum_metadata(root)

def node_value(node):
    '''
    If a node has no child nodes, its value is the sum of its metadata entries.
    If a node does have child nodes, its value is the sum of the values of 
    the child nodes referenced by the metadata entries.
    '''
    if not node.children:
        return sum(node.metadata)
    else:
        return sum(node_value(node.children[i - 1]) for i in node.metadata 
                if i > 0 and i <= len(node.children))


def part2(license_file):
    data  = [int(i) for i in re.findall(r'\d+', license_file)]

    root = parse_tree(data) 
    return node_value(root)

if __name__ == '__main__':
    with open('../input/d08.txt', mode='r') as f:
        _input = f.read().strip()

    print('Part One: {}'.format(part1(_input)))
    print('Part Two: {}'.format(part2(_input)))

