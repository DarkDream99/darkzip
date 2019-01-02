class HuffmanEncoder(object):

    def __init__(self, huffman_table, source_text):
        self.huffman_table = huffman_table
        self.source_text = source_text

    def encode(self):
        encoded_str = ""
        for symbol in self.source_text:
            if symbol not in self.huffman_table:
                raise ValueError("Haffman table doesn't contain this symbol")
            encoded_str += self.huffman_table[symbol]

        return encoded_str
