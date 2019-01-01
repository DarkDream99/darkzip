import json
import jsonpickle
import math
import os
import re

from decimal import Decimal
from decimal import getcontext
from collections import Counter

from .dfile import DarkFile
from .dfolder import DarkFolder


class Archiver:

    def __init__(self, folder_path, folder_title):
        self.folder_path = folder_path
        self.folder_title = folder_title
        getcontext().prec = 2_000_000

    @staticmethod
    def create_darkzip_file(file_obj):
        zip_path = os.path.join("out", file_obj.title[:file_obj.title.rindex('.')] + ".dzf")
        with open(zip_path, "w", encoding="utf-8") as file:
            str_data = json.dumps(file_obj.__dict__)
            file.write(str_data)

    @staticmethod
    def archive_file(file, file_name):
        strings = ""
        for line in file:
            strings += line

        file_obj = DarkFile(strings, file_name)
        return file_obj

    @staticmethod
    def dearchive_file(zip_path, zip_file_name):
        with open(os.path.join(zip_path, zip_file_name)) as zip_file:
            zip_file_obj = json.load(zip_file)

        path = os.path.join("decompress", zip_file_obj["title"])
        with open(path, "w+", encoding="utf-8") as file:
            file.writelines(zip_file_obj["text"])

    @staticmethod
    def _dir_path(path):
        pattern = r"(\./)|(\\)"
        dirs = re.split(pattern, path)
        dirs = list(
            filter(
                lambda it: it is not None and it != "./" and it != "\\" and it,
                dirs
            )
        )

        return dirs

    @staticmethod
    def create_darkzip_folder(compressed_folder):
        json_folder = json.dumps(compressed_folder.json_object, ensure_ascii=False)  # jsonpickle.encode(compressed_folder)
        with open(os.path.join("./out", compressed_folder.title + ".dzf"), "w+", encoding="utf-8") as file:
            file.writelines(json_folder)

    @staticmethod
    def archive_folder(folder_path, folder_title):
        folder_obj = DarkFolder([], [], folder_title)
        dir_tree = os.walk(folder_path)

        for path, folder_titles, file_titles in dir_tree:
            folders_path = Archiver._dir_path(path)
            folder_ptr = folder_obj

            is_root = True

            for folder_name in folders_path:
                if is_root:
                    is_root = False
                    continue
                for folder in folder_obj.folders:
                    if folder.title == folder_name:
                        folder_ptr = folder

            for folder_title in folder_titles:
                folder_ptr.folders.append(DarkFolder([], [], folder_title))

            for file_title in file_titles:
                with open(os.path.join(path, file_title), "r", encoding="utf-8") as file:
                    compressed_file = Archiver.archive_file(file, file_title)
                folder_ptr.files.append(compressed_file)

        Archiver.create_darkzip_folder(folder_obj)
        return folder_obj

    @staticmethod
    def dearchive_folder(folder, path_out):
        folder_path = os.path.join(path_out, folder["title"])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for file in folder["files"]:
            file_path = os.path.join(folder_path, file["title"])
            with open(file_path, "w+", encoding="utf-8") as hfile:
                hfile.writelines(file["text"])

        for next_folder in folder["folders"]:
            next_out_path = os.path.join(folder_path)
            Archiver.dearchive_folder(next_folder, next_out_path)

    @staticmethod
    def delta_coding(file_path=os.path.join("out", "test_dirs.dzf")):
        bytes_ls = []

        with open(file_path, "rb") as file:
            next_byte = file.read(1)

            while next_byte:
                bytes_ls.append(next_byte[0])
                next_byte = file.read(1)

        new_bytes = [bytes_ls[0]]
        for i in range(1, len(bytes_ls)):
            new_bytes.append(bytes_ls[i] - bytes_ls[i - 1])

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(new_bytes))

    @staticmethod
    def next_interval_code(distance, prev_byte, next_byte,
                           comm_chances, chances):
        if not prev_byte:
            left_bound = distance[0]
        else:
            left_bound = distance[0] + (distance[1] - distance[0]) * comm_chances[prev_byte]
        right_bound = left_bound + (distance[1] - distance[0]) * chances[next_byte]

        return [left_bound, right_bound]

    @staticmethod
    def interval_coding(file_path=os.path.join("out", "test_dirs.dzf")):
        byte_ls = json.load(open(file_path, "r"))
        counter = Counter(byte_ls)
        all_counts = sum(counter.values())

        chances = dict()
        for item in counter:
            float_number = round(counter[item] / all_counts, 6)
            chances[item] = Decimal(str(float_number))

        base_distance = [Decimal('0'), Decimal('1')]
        next_dist = base_distance

        unic_byte_ls = sorted(list(set(byte_ls)))
        prev_byte_ls = dict()
        prev_byte_ls[unic_byte_ls[0]] = None
        for i in range(1, len(unic_byte_ls)):
            prev_byte_ls[unic_byte_ls[i]] = unic_byte_ls[i - 1]

        comm_chances = dict()
        comm_chance = Decimal("0")
        for byte in unic_byte_ls:
            comm_chance += chances[byte]
            comm_chances[byte] = comm_chance

        for byte in byte_ls:
            next_dist = Archiver.next_interval_code(
                next_dist, prev_byte_ls[byte], byte, comm_chances, chances)

        chances_out = dict()
        for byte in chances:
            chances_out[byte] = str(chances[byte])

        data_out = dict()
        data_out["length"] = len(byte_ls)
        data_out["chances"] = chances_out
        data_out["interval"] = str((next_dist[0] + next_dist[1]) / 2)

        json.dump(data_out, open(file_path, "w", encoding="utf-8"))

    @staticmethod
    def find_dist_for_interval(distance, interval, unic_byte_ls, prev_byte_ls,
                               comm_chances, chances):
        left_bound = 0
        right_bound = len(unic_byte_ls)

        while right_bound - left_bound >= 0:
            mid = left_bound + (right_bound - left_bound) // 2
            byte = unic_byte_ls[mid]
            new_dist = Archiver.next_interval_code(distance, prev_byte_ls[byte], byte, comm_chances, chances)

            if new_dist[0] <= interval < new_dist[1]:
                return byte, new_dist

            if interval < new_dist[0]:
                right_bound = mid - 1
            elif interval >= new_dist[1]:
                left_bound = mid + 1

        return None, None

    @staticmethod
    def interval_decoding(file_path):
        json_data = json.load(open(file_path, "r"))

        base_dist = [Decimal('0'), Decimal('1')]
        next_dist = base_dist
        unic_byte_ls = sorted(int(byte) for byte in list(json_data["chances"].keys()))

        prev_byte_ls = dict()
        prev_byte_ls[unic_byte_ls[0]] = None
        for i in range(1, len(unic_byte_ls)):
            prev_byte_ls[unic_byte_ls[i]] = unic_byte_ls[i - 1]

        chances = dict()
        for byte in json_data["chances"]:
            chances[int(byte)] = Decimal(json_data["chances"][byte])

        comm_chances = dict()
        comm_chance = Decimal("0")
        for byte in unic_byte_ls:
            comm_chance += chances[byte]
            comm_chances[byte] = comm_chance

        byte_count = json_data["length"]
        interval = Decimal(json_data["interval"])
        source_bytes = []
        while byte_count != 0:
            byte, new_dist = Archiver.find_dist_for_interval(
                base_dist, interval, unic_byte_ls, prev_byte_ls,
                comm_chances, chances
            )

            if byte is None:
                break
            source_bytes.append(byte)
            interval = (interval - new_dist[0]) / (new_dist[1] - new_dist[0])

            # for byte in unic_byte_ls:
            #     new_dist = Archiver.next_interval_code(base_dist, prev_byte_ls[byte], byte, comm_chances, chances)
            #     if new_dist[0] <= interval < new_dist[1]:
            #         # next_dist = new_dist
            #         source_bytes.append(byte)
            #         # code = (code - RangeLow(x)) / (RangeHigh(x) - RangeLow(x))
            #         interval = (interval - new_dist[0]) / (new_dist[1] - new_dist[0])
            #         break
            #
            byte_count -= 1

        json.dump(source_bytes, open(file_path, "w", encoding="utf-8"))
