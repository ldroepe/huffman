import argparse

class Node:
    '''
    Simple Binary tree Node class for creating the encoding tree
    '''

    def __init__(self, char, count, left = None, right = None):

        self.char = char
        self.count = count

        self.left = left
        self.right = right
    
    def __str__(self):

        return f'({self.char} -> {self.count}. Left: {self.left}, Right: {self.right})'
    
    def __repr__(self):

        return self.__str__()

# End Node class


def main(**args):

    tree = build_tree(args['f'])

    print(tree)

def build_tree(filename):
    '''
    Build corresponding encoding/decoding tree that will be used
    for encoding/decoding of this particular file

    :param filename: where to read chars from
    :return: huffman tree
    '''

    counts = count_chars(filename)
    pairs = [(x, counts[x]) for x in counts]

    #sort values by count
    #put low values at end so we can use pairs.pop()
    pairs.sort(key = lambda x: x[1], reverse=True)

    while len(pairs) > 1:
        
        first = pairs.pop()
        first_node = build_node(first)

        second = pairs.pop()
        second_node = build_node(second)

        #build parent node and put back into the list
        parent = Node(None, get_count(first) + get_count(second), first_node, second_node)
        insertion_index = find_insertion(pairs, get_count(parent))

        pairs.insert(insertion_index, parent)


    return pairs.pop()

def count_chars(file):
    '''
    Count the number of times a character appears in the given file

    :param file: file to read chars from
    :return: dict mapping char to occurrence
    '''

    counts = {}
    inFile = open(file, 'r')
    
    for line in inFile:
        for char in line:
            
            count = counts.get(char, 0)
            count += 1
            counts[char] = count

    return counts

def build_node(pair):
    '''
    Takes a pair tuple (character, count) and returns a Node to be
    placed in the tree

    :param pair: tuple pair of (characcter, count)
    :return: corresponding Node
    '''

    #convert the tuple
    if type(pair) is tuple:

        return Node(pair[0], pair[1])

    #object is _probably_ already a Node
    else:

        return pair

def find_insertion(pairs, count):
    '''
    Determines where in the list of pairs the new parent node should be inserted into

    :param pairs: list of pairs / nodes
    :param count: combined count of new parent node
    :return: index to insert parent node at
    '''

    for (i, val) in enumerate(pairs):

        val_count = get_count(val)
        if (val_count < count):
            return i

    return -1 #insert at end of list

def get_count(obj):
    '''
    Get count of this character / node

    :param obj: object to get count of
    :return: count of character / node
    '''

    if type(obj) is tuple:

        return obj[1]

    elif type(obj) is Node:
        
        return obj.count

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Huffman Encoder')
    parser.add_argument('-f', type=str, required=True, help='file to read text from')

    args = parser.parse_args()

    main(**vars(args))
