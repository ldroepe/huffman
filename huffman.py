import os
import sys
import pickle
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

    efile = args['e'] #file to encode
    dfile = args['d'] #file to decode

    #encode
    if efile:

        #encode the file
        tree = build_tree(efile)

        print(sys.getsizeof(tree))

        encoding = encode(efile, tree)
        encoding = encoding.encode('utf-8')

        print(sys.getsizeof(encoding))

        outFile = open(os.path.splitext(efile)[0]+'.enc', 'wb')
        
        #write info
        pickle.dump(tree, outFile)
        outFile.write(encoding)
    
    #decode
    elif dfile:

        #read info
        inFile = open(dfile, 'rb')

        tree = pickle.load(inFile)
        encoding = inFile.read()
        encoding = encoding.decode('utf-8') #easier to work with strings

        decoding = decode(tree, encoding)

        outFile = open(os.path.splitext(dfile)[0]+'_dec.txt', 'w')
        outFile.write(decoding)

def build_tree(filename):
    '''
    Build corresponding encoding/decoding tree that will be used
    for encoding/decoding of this particular file

    :param filename: where to read chars from
    :return: huffman tree
    '''

    counts = count_chars(filename)
    characters = counts.keys() #list of characters in the file
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

    return len(pairs) #insert at end of list

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


def encode(filename, tree):
    '''
    Actually encode the file that was specified

    :param filename: name of file to encode
    :param tree: encoding tree for filename
    '''

    inFile = open(filename)
    character_encodings = {}
    build_encodings(tree, character_encodings)

    full_encoding = ''

    for line in inFile:
        for char in line:
            
            encoding = character_encodings.get(char, None)
            full_encoding += encoding

    return full_encoding

def build_encodings(tree, character_encodings):
    '''
    Build the encodings for each character according to the encoding tree

    :param tree: encoding / decoding tree
    :param character_encodings: encodings of each character
    '''

    _encoding_helper(tree, character_encodings, '')
    
def _encoding_helper(current, character_encodings, encoding):
    '''
    Helper method to build_encodings
    Recursively traverses encoding tree to find encodings of each character

    :param current: current node in the tree
    :param character_encodings: encodings of each character
    :param encoding: current, working encoding of a character
    '''

    #stop the recursion
    if current is None:
        return

    char = current.char

    #place character in the character_encodings dict
    if not(current.char is None):
        character_encodings[char] = encoding

    #look for characters in subtrees
    if not(current.left is None):
        _encoding_helper(current.left, character_encodings, encoding+'0')

    if not(current.right is None):
        _encoding_helper(current.right, character_encodings, encoding+'1')

def decode(tree, encoding):
    '''
    Decode an encoded file with the tree that was provided

    :param tree: encoding tree to be used for decoding
    :param encoding: encoding to decode
    :return: decoded file
    '''

    decoding = ''
    current = tree

    for char in encoding:

        if char == '1':
            current = current.right

        elif char == '0':
            current = current.left

        if not(current.char is None):
            
            decoding += current.char
            current = tree

    return decoding


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Huffman Encoder')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-e', type=str, help='encode a file')
    group.add_argument('-d', type=str, help='decode a file')

    args = parser.parse_args()

    main(**vars(args))
