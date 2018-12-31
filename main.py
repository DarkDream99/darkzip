from archiver.archiver import Archiver
from archiver.haffman_tree import HaffmanTree
from archiver.haffman_table import HaffmanTable
from archiver.haffman_coder import HaffmanEncoder
from archiver.haffman_tree import END_SYMBOL
from archiver.byter import Byter
from collections import Counter


CODE = "c"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"


def run():
    command = NOT_USE
    dark_archiver = Archiver(None, None)
    while command != EXIT:
        line = input(">> ")
        params = line.split(' ')

        # try:
        if params[0] == CODE:
            path = params[1]
            title = params[2]
            dark_archiver.archive_folder(path, title)
            dark_archiver.delta_coding()
            dark_archiver.interval_coding()

        if params[0] == DECODE:
            file_path = params[1]
            dark_archiver.interval_decoding(file_path)
        # except Exception as e:
        #     print(e)


def test_haffman():
    symbols = []
    with open("test.txt", "r", encoding="utf-8") as file:
        for line in file:
            symbols.extend(line)

    counter = Counter(symbols)
    haffman_tree = HaffmanTree(counter)
    leaves = haffman_tree.leaves
    haffman_table = HaffmanTable(leaves)

    encoder = HaffmanEncoder(haffman_table, symbols)
    encoded_str = encoder.encode()

    byter = Byter()
    encoded_bytes = byter.convert_to_bytes(encoded_str)
    print(encoded_bytes)

    encoded_haffman_tree = haffman_tree.tree_code()
    print(encoded_haffman_tree)

    print(END_SYMBOL)

    with open("encode.txt", "wb+") as file:
        for byte in encoded_haffman_tree:
            file.write(byte.to_bytes(1, "little"))

        for byte in END_SYMBOL:
            file.write(byte.to_bytes(1, "little"))

        for byte in encoded_bytes:
            file.write(byte.to_bytes(1, "little"))


test_haffman()

# print("шпр".find("kр"))

# print(int("100", 2))

# a = (164).to_bytes(1, "little")
# print(a)
# print(bytes('DUDD{', encoding="utf-8"))
# with open("test.txt", "wb+") as file:
#     file.write(bytes('Ъ', encoding="utf-8"))
#     file.write(bytes('\'', encoding="utf-8"))
#
# with open("test.txt", "rb") as file:
#     a = file.read(2)
#     print(a == bytes('Ъ', encoding="utf-8"))
#     a = file.read(1)
#     print(a == b'\'')
#
# print(bin(10)[2:])
