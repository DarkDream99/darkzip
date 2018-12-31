class HaffmanEncoder(object):

    def __init__(self, haffman_table, source_text):
        self.haffman_table = haffman_table
        self.source_text = source_text

    def encode(self):
        encoded_str = ""
        for symbol in self.source_text:
            if symbol not in self.haffman_table:
                raise ValueError("Haffman table doesn't contain this symbol")
            encoded_str += self.haffman_table[symbol]

        return encoded_str
