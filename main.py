from archiver.runner import Runner


CODE = "c"
DECODE = "d"
EXIT = "e"
NOT_USE = "-"


def run():
    command = NOT_USE
    runner = Runner()
    settings = dict()

    while command != EXIT:
        line = input(">> ")
        params = line.split(maxsplit=1)

        if params[0] == CODE:
            modules = params[1].split('=')
            for ind, m in enumerate(modules):
                if m.strip() == "path":
                    settings["path"] = modules[ind + 1].strip()

            runner.encode_folder(**settings)

        if params[0] == DECODE:
            modules = params[1].split('=')
            for ind, m in enumerate(modules):
                if m.strip() == "path":
                    settings["path"] = modules[ind + 1].strip()
                if m.strip() == "out":
                    settings["out"] = modules[ind + 1].strip()

            runner.decode_folder(**settings)


run()
