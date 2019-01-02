import sys
import os

import checker

from archiver.runner import Runner


CODE = "c"
COMPARE = "cmp"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"


def is_file(file_path):
    return os.path.isfile(file_path)


def take_settings(modules):
    settings = dict()
    prev_command = None
    for ind, m in enumerate(modules):
        items = m.split()
        if prev_command is None:
            prev_command = items[-1]
            continue

        curr_param = ""
        for ind in range(len(items)):
            if ind != len(items) - 1 or len(items) == 1:
                curr_param += items[ind] + " "

        settings[prev_command.strip()] = curr_param.strip()
        prev_command = items[-1]
    return settings


line = " ".join(sys.argv[1:])
print(line)
settings = dict()
is_file_command = False
runner = Runner()
params = line.split(maxsplit=1)

if params[0] == CODE:
    modules = params[1].split('=')
    base_settings = take_settings(modules)

    if "path" in base_settings:
        if is_file(base_settings["path"]):
            settings["file_encode_path"] = base_settings["path"]
            is_file_command = True
        else:
            settings["folder_encode_path"] = base_settings["path"]

    if is_file_command:
        runner.encode_file(**settings)
    else:
        runner.encode_folder(**settings)

if params[0] == DECODE:
    modules = line.split('=')
    base_settings = take_settings(modules)

    if "path" in base_settings:
        settings["folder_decode_path"] = base_settings["path"]
    if "out" in base_settings:
        settings["folder_decode_out_path"] = base_settings["out"]

    runner.decode_folder(**settings)

if params[0] == COMPARE:
    modules = line.split('=')
    base_settings = take_settings(modules)

    path_file_a = ""
    path_file_b = ""

    if "path_a" in base_settings:
        path_file_a = base_settings["path_a"]
    if "path_b" in base_settings:
        path_file_b = base_settings["path_b"]

    if checker.check_files(path_file_a, path_file_b):
        print("Equal files")
    else:
        print("Not equal files")

# def run():
#     command = NOT_USE
#     runner = Runner()
#     settings = dict()
#
#     while command != EXIT:
#         settings.clear()
#         line = input(">> ")
#         params = line.split(maxsplit=1)
#         is_file_command = False
#
#         if params[0] == CODE:
#             modules = params[1].split('=')
#             base_settings = take_settings(modules)
#
#             if "path" in base_settings:
#                 if is_file(base_settings["path"]):
#                     settings["file_encode_path"] = base_settings["path"]
#                     is_file_command = True
#                 else:
#                     settings["folder_encode_path"] = base_settings["path"]
#
#             if is_file_command:
#                 runner.encode_file(**settings)
#             else:
#                 runner.encode_folder(**settings)
#
#         if params[0] == DECODE:
#             modules = line.split('=')
#             base_settings = take_settings(modules)
#
#             if "path" in base_settings:
#                 settings["folder_decode_path"] = base_settings["path"]
#             if "out" in base_settings:
#                 settings["folder_decode_out_path"] = base_settings["out"]
#
#             runner.decode_folder(**settings)
#
#         if params[0] == COMPARE:
#             modules = line.split('=')
#             base_settings = take_settings(modules)
#
#             path_file_a = ""
#             path_file_b = ""
#
#             if "path_a" in base_settings:
#                 path_file_a = base_settings["path_a"]
#             if "path_b" in base_settings:
#                 path_file_b = base_settings["path_b"]
#
#             if checker.check_files(path_file_a, path_file_b):
#                 print("Equal files")
#             else:
#                 print("Not equal files")
#
#
# run()
