import sys
import os

from archiver.runner import Runner


CODE = "c"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"


def is_file(file_path):
    return os.path.isfile(file_path)


line = " ".join(sys.argv[1:])
print(line)
settings = dict()
is_file_command = False
runner = Runner()
params = line.split(maxsplit=1)

if params[0] == CODE:
    modules = params[1].split('=')
    for ind, m in enumerate(modules):
        if m.strip() == "path":
            if is_file(modules[ind + 1].strip()):
                settings["file_encode_path"] = modules[ind + 1].strip()
                is_file_command = True
            else:
                settings["folder_encode_path"] = modules[ind + 1].strip()

    if is_file_command:
        runner.encode_file(**settings)
    else:
        runner.encode_folder(**settings)

if params[0] == DECODE:
    prev_command = None
    modules = line.split('=')
    for ind, m in enumerate(modules):
        items = m.split()
        if prev_command is None:
            prev_command = items[-1]
            continue

        curr_param = ""
        for ind in range(len(items)):
            if ind != len(items) - 1 or len(items) == 1:
                curr_param += items[ind] + " "

        if prev_command.strip() == "path":
            settings["folder_decode_path"] = curr_param.strip()
        if prev_command.strip() == "out":
            settings["folder_decode_out_path"] = curr_param.strip()

        prev_command = items[-1]

    runner.decode_folder(**settings)


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
#             for ind, m in enumerate(modules):
#                 if m.strip() == "path":
#                     if is_file(modules[ind + 1].strip()):
#                         settings["file_encode_path"] = modules[ind + 1].strip()
#                         is_file_command = True
#                     else:
#                         settings["folder_encode_path"] = modules[ind + 1].strip()
#
#             if is_file_command:
#                 runner.encode_file(**settings)
#             else:
#                 runner.encode_folder(**settings)
#
#         if params[0] == DECODE:
#             prev_command = None
#             modules = line.split('=')
#             for ind, m in enumerate(modules):
#                 items = m.split()
#                 if prev_command is None:
#                     prev_command = items[-1]
#                     continue
#
#                 curr_param = ""
#                 for ind in range(len(items)):
#                     if ind != len(items) - 1 or len(items) == 1:
#                         curr_param += items[ind] + " "
#
#                 if prev_command.strip() == "path":
#                     settings["folder_decode_path"] = curr_param.strip()
#                 if prev_command.strip() == "out":
#                     settings["folder_decode_out_path"] = curr_param.strip()
#
#                 prev_command = items[-1]
#
#             runner.decode_folder(**settings)
#
#
# run()
