import time


class HuffmanEncoder(object):

    def __init__(self, huffman_table, source_text):
        self.huffman_table = huffman_table
        self.source_text = source_text

    def encode(self):
        encoded_arr = []
        ind = 1

        start = time.time()
        for symbol in self.source_text:
            if symbol not in self.huffman_table:
                raise ValueError("Haffman table doesn't contain this symbol")
            encoded_arr.append(self.huffman_table[symbol])

            if ind % 1000 == 0:
                print(f"{ind} / {len(self.source_text)}")
            ind += 1

        encoded_str = "".join(encoded_arr)
        end = time.time()
        print(f"Data was encoded: {end - start}")
        return encoded_str
