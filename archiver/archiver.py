import json
import os
import re

from .dfile import DarkFile
from .dfolder import DarkFolder


class Archiver:

    def __init__(self, folder_path, folder_title):
        self.folder_path = folder_path
        self.folder_title = folder_title

    @staticmethod
    def create_darkzip_file(file_obj):
        zip_path = os.path.join("out", file_obj.title[:file_obj.title.rindex('.')] + ".dzf")
        with open(zip_path, "w", encoding="cp1251") as file:
            str_data = json.dumps(file_obj.__dict__)
            file.writelines(str_data)

    @staticmethod
    def archive_file(file_path, create_mode=False):
        file_title = Archiver._dir_path(file_path)[-1]

        strings = ""
        with open(file_path, "r", encoding="cp1251") as file:
            for line in file:
                strings += line

        file_obj = DarkFile(strings, file_title)
        base_folder = DarkFolder([file_obj], [], "")
        if create_mode:
            Archiver.create_darkzip_folder(base_folder, file_obj.name)
        return file_obj

    @staticmethod
    def dearchive_file(zip_path, zip_file_name):
        with open(os.path.join(zip_path, zip_file_name)) as zip_file:
            zip_file_obj = json.load(zip_file)

        path = os.path.join("decompress", zip_file_obj["title"])
        with open(path, "w+", encoding="cp1251") as file:
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
    def create_darkzip_folder(compressed_folder, title=None):
        json_folder = json.dumps(compressed_folder.json_object, ensure_ascii=False)
        file_title = compressed_folder.title + ".dzf"
        if title is not None:
            file_title = title + ".dzf"
        with open(os.path.join("./out", file_title), "w+", encoding="cp1251") as file:
            file.writelines(json_folder)

    @staticmethod
    def archive_folder(folder_path):
        source_folder_title = Archiver._dir_path(folder_path)[-1]
        folder_obj = DarkFolder([], [], source_folder_title)
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
                compressed_file = Archiver.archive_file(os.path.join(path, file_title))
                folder_ptr.files.append(compressed_file)

        Archiver.create_darkzip_folder(folder_obj)
        return source_folder_title, folder_obj

    @staticmethod
    def dearchive_folder(folder, path_out):
        folder_path = os.path.join(path_out, folder["title"])
        if not os.path.exists(folder_path) and folder["title"] != "":
            os.makedirs(folder_path)

        for file in folder["files"]:
            file_path = os.path.join(folder_path, file["title"])
            with open(file_path, "w+", encoding="cp1251") as hfile:
                hfile.writelines(file["text"])

        for next_folder in folder["folders"]:
            next_out_path = os.path.join(folder_path)
            Archiver.dearchive_folder(next_folder, next_out_path)
