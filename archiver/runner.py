import json
import os

from archiver.archiver import Archiver
from archiver.huffmancompressor import HuffmanCompressor
from archiver.huffman_reader import HuffmanReader
from archiver.huffman_writer import HuffmanWriter
from archiver.byter import Byter


class Runner(object):

    def __init__(self):
        self.dark_archiver = Archiver(None, None)
        self.folder_encode_path = "test_dirs"
        self.folder_encode_out_path = None
        self.folder_decode_path = "out/test_dirs.dzf"
        self.folder_decode_out_path = "decode"

        self.file_encode_path = "test.txt"

    def encode_file(self, **kwargs):
        if "file_encode_path" in kwargs:
            self.file_encode_path = kwargs["file_encode_path"]
        if "folder_encode_out_path" in kwargs:
            self.folder_encode_out_path = kwargs["folder_encode_out_path"]

        file_name = self.dark_archiver.archive_file(self.file_encode_path, create_mode=True).name
        if self.folder_encode_out_path is None:
            out_file_path = os.path.join(os.path.dirname(self.file_encode_path), file_name + ".dzf")
        else:
            out_file_path = os.path.join(self.folder_encode_out_path, file_name + ".dzf")

        file_path = os.path.join("out", file_name + ".dzf")
        self._encode(file_path, out_file_path)

    def encode_folder(self, **kwargs):
        if "folder_encode_path" in kwargs:
            self.folder_encode_path = kwargs["folder_encode_path"]
        if "folder_encode_out_path" in kwargs:
            self.folder_encode_out_path = kwargs["folder_encode_out_path"]

        folder_title = self.dark_archiver.archive_folder(self.folder_encode_path)[0]
        file_path = os.path.join("out", folder_title + ".dzf")

        if self.folder_encode_out_path is None:
            out_file_path = os.path.join(self.folder_encode_path + ".dzf")
        else:
            out_file_path = os.path.join(self.folder_encode_out_path, folder_title + ".dzf")
        self._encode(file_path, out_file_path)

    def _encode(self, file_path, encode_out_path):
        symbols = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                symbols.extend(line)

        compressor = HuffmanCompressor(source_text=symbols)
        encoded_str = compressor.encode()

        byter = Byter()
        encoded_bytes = byter.convert_to_bytes(encoded_str)
        encoded_huffman_tree = compressor.huffman_tree_code
        encoded_count_bytes = self._convert_to_225(len(encoded_str))

        HuffmanWriter.write(
            encode_out_path, encoded_bytes,
            encoded_huffman_tree, encoded_count_bytes
        )

    def decode_folder(self, **kwargs):
        if "folder_decode_path" in kwargs:
            self.folder_decode_path = kwargs["folder_decode_path"]
        if "folder_decode_out_path" in kwargs:
            self.folder_decode_out_path = kwargs["folder_decode_out_path"]

        file_bytes = b""
        with open(self.folder_decode_path, "rb") as file:
            next_byte = file.read(1)
            while next_byte:
                file_bytes += next_byte
                next_byte = file.read(1)

        huffman_reader = HuffmanReader(file_bytes)
        compressor = HuffmanCompressor(huffman_tree_bytes=huffman_reader.tree_bytes)

        byter = Byter()
        bit_str_bytes = huffman_reader.count_bytes
        bit_str = byter.convert_to_bit_str(
            huffman_reader.code_bytes,
            self._convert_from_255(bit_str_bytes)
        )

        source_str = compressor.decode(bit_str)
        folder_json = json.loads(source_str)

        self.dark_archiver.dearchive_folder(folder_json, self.folder_decode_out_path)
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

