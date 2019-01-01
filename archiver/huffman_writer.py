from .huffman_reader import END_SYMBOL


class HuffmanWriter(object):

    @staticmethod
    def write(file_path, encoded_bytes, encoded_huffman_tree, encoded_count_bytes):
        with open(file_path, "wb+") as file:
            for byte in encoded_huffman_tree:
                file.write(byte.to_bytes(1, "little"))

            for byte in END_SYMBOL:
                file.write(byte.to_bytes(1, "little"))

            for byte in encoded_count_bytes:
                file.write(byte.to_bytes(1, "little"))

            for byte in END_SYMBOL:
                file.write(byte.to_bytes(1, "little"))

            for byte in encoded_bytes:
                file.write(byte.to_bytes(1, "little"))
