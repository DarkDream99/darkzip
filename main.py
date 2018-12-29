from archiver.archiver import Archiver


CODE = "c"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"

command = NOT_USE
dark_archiver = Archiver
while command != EXIT:
    line = input(">> ")
    params = line.split(' ')

    try:
        if params[0] == CODE:
            path = params[1]
            title = params[2]
            dark_archiver.archive_folder(path, title)
            dark_archiver.delta_coding()
            dark_archiver.interval_coding()

        if params[0] == DECODE:
            file_path = params[1]
            dark_archiver.interval_decoding(file_path)
    except Exception as e:
        print(e)
