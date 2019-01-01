def _read_file_bytes(file_path):
    file_bytes = b""
    with open(file_path, "rb") as file:
        next_byte = file.read(1)
        while next_byte:
            file_bytes += next_byte
            next_byte = file.read(1)
    return file_bytes


def check_files(file_path_a, file_path_b):
    bytes_a = _read_file_bytes(file_path_a)
    bytes_b = _read_file_bytes(file_path_b)

    return bytes_a == bytes_b
