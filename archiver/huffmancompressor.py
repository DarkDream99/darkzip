from collections import Counter

from .huffman_coder import HuffmanEncoder
from .huffman_decoder import HuffmanDecoder
from .huffman_tree import HuffmanTree
from .huffman_table import HuffmanTable


class HuffmanCompressor(HuffmanEncoder, HuffmanDecoder):

    def __init__(self, source_text="", huffman_tree_bytes=""):
        counter = Counter(source_text)
        if huffman_tree_bytes == "":
            huffman_tree = HuffmanTree(counter)
        else:
            huffman_tree = HuffmanTree(huffman_tree_bytes)
        leaves = huffman_tree.leaves
        huffman_table = HuffmanTable(leaves)

        HuffmanEncoder.__init__(self, huffman_table, source_text)
        HuffmanDecoder.__init__(self, huffman_tree)

    @property
    def huffman_tree_code(self):
        return self.huffman_tree.tree_code()
