import json

from archiver.archiver import Archiver
from archiver.dfolder import DarkFolder
from archiver.huffman_tree import HuffmanTree
from archiver.huffman_table import HuffmanTable
from archiver.huffman_coder import HuffmanEncoder
from archiver.huffman_decoder import HuffmanDecoder
from archiver.huffman_reader import HuffmanReader
from archiver.huffman_reader import END_SYMBOL
from archiver.byter import Byter
from collections import Counter


class Runner(object):

    def __init__(self):
        self.dark_archiver = Archiver(None, None)

    def encode_file(self, file_path):
        ...

    def decode_file(self, file_path):
        ...

    def encode_folder(self, folder_path):
        self.dark_archiver.archive_folder(folder_path)

        symbols = []
        with open("out/test_dirs.dzf", "r", encoding="utf-8") as file:
            for line in file:
                symbols.extend(line)

        counter = Counter(symbols)
        huffman_tree = HuffmanTree(counter)
        leaves = huffman_tree.leaves
        huffman_table = HuffmanTable(leaves)

        encoder = HuffmanEncoder(huffman_table, symbols)
        encoded_str = encoder.encode()

        byter = Byter()
        encoded_bytes = byter.convert_to_bytes(encoded_str)
        encoded_huffman_tree = huffman_tree.tree_code()
        encoded_count_bytes = self._convert_to_225(len(encoded_str))

        with open("out/test_dirs.dzf", "wb+") as file:
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

    def decode_folder(self, folder_path="out/test_dirs.dzf"):
        file_bytes = b""
        with open(folder_path, "rb") as file:
            next_byte = file.read(1)
            while next_byte:
                file_bytes += next_byte
                next_byte = file.read(1)

        huffman_reader = HuffmanReader(file_bytes)

        huffman_tree = HuffmanTree(huffman_reader.tree_bytes)
        byter = Byter()

        bit_str_bytes = huffman_reader.count_bytes
        bit_str = byter.convert_to_bit_str(
            huffman_reader.code_bytes,
            self._convert_from_255(bit_str_bytes)
        )

        huffman_decoder = HuffmanDecoder(huffman_tree)
        source_str = huffman_decoder.decode(bit_str)

        folder_json = json.loads(source_str)

        self.dark_archiver.dearchive_folder(folder_json, "dearchive")
        with open("out/test_dirs.dzf", "w+", encoding="utf-8") as file:
            file.writelines(source_str)

    @staticmethod
    def _convert_to_225(num):
        num_225 = []
        while num > 0:
            num_225.append(num % 225)
            num //= 225
        return num_225

    @staticmethod
    def _convert_from_255(nums):
        res = 0
        power = 0

        for i, num in enumerate(nums):
            res += num * 225 ** power
            power += 1

        return res

