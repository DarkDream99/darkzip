class Byter(object):

    def __init__(self):
        self.BYTE_SIZE = 8

    def convert_to_bytes(self, byte_str):
        ind = 0
        res_bytes = b""

        while ind < len(byte_str):
            next_byte_str = byte_str[ind: ind + self.BYTE_SIZE]
            dec_number = int(next_byte_str, 2)
            res_bytes += dec_number.to_bytes(1, "little")
            ind += self.BYTE_SIZE

        return res_bytes
