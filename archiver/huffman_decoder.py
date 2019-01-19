import time


class HuffmanDecoder(object):

    def __init__(self, huffman_tree):
        self.huffman_tree = huffman_tree

    def decode(self, bit_str):
        bit_ind = 0
        source_arr = []

        start = time.time()
        while bit_ind != len(bit_str):
            start_node = self.huffman_tree.head
            while not start_node.is_leaf() and bit_ind != len(bit_str):
                next_bit = bit_str[bit_ind]
                if next_bit == '0':
                    start_node = start_node.left_child
                else:
                    start_node = start_node.right_child
                bit_ind += 1

            source_arr.extend(start_node.symbol)

        source_str = "".join(source_arr)
        end = time.time()
        print(f"Decoded was finished: {end - start}")
        return source_str
