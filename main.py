from archiver.runner import Runner


CODE = "c"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"


def run():
    command = NOT_USE
    runner = Runner()

    while command != EXIT:
        line = input(">> ")
        params = line.split(' ')

        if params[0] == CODE:
            path = params[1]
            runner.encode_folder(path)

        if params[0] == DECODE:
            runner.decode_folder()


run()
