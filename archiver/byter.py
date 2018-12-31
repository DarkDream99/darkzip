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

    def convert_to_bit_str(self, code_bytes, bit_str_len):
        res_bit_str = ""

        for ind, byte in enumerate(code_bytes):
            dec_byte = byte[0]
            next_bit_str = bin(dec_byte)[2:]
            if ind < len(code_bytes) - 1:
                next_bit_str = next_bit_str.rjust(self.BYTE_SIZE, '0')
            else:
                curr_size = ind * self.BYTE_SIZE
                next_bit_str = next_bit_str.rjust(bit_str_len - curr_size, '0')
            res_bit_str += next_bit_str

        return res_bit_str
