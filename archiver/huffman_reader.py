SEPARATOR = (0).to_bytes(1, "little")
END_SYMBOL = (2).to_bytes(1, "little") + (2).to_bytes(1, "little") + (8).to_bytes(1, "little")


class HuffmanReader(object):

    def __init__(self, source_bytes):
        next_ind, self.haffman_tree_bytes = self._read_haffman_tree(source_bytes)
        next_ind, self.count_in_bytes = self._read_counts(source_bytes, next_ind)
        self.haffman_code_bytes = self._read_codes(source_bytes, next_ind)

    @staticmethod
    def _read_haffman_tree(source_bytes):
        ind = 0
        haffman_bytes = []
        while ind < len(source_bytes) - 2:
            byte_a = (source_bytes[ind]).to_bytes(1, "little")
            byte_b = (source_bytes[ind + 1]).to_bytes(1, "little")
            byte_c = (source_bytes[ind + 2]).to_bytes(1, "little")

            if byte_a + byte_b + byte_c == END_SYMBOL:
                break

            haffman_bytes.append(source_bytes[ind].to_bytes(1, "little"))
            ind += 1

        return ind + 3, haffman_bytes

    @staticmethod
    def _read_counts(source_bytes, start_ind):
        count_bytes = []

        while start_ind < len(source_bytes):
            byte_a = (source_bytes[start_ind]).to_bytes(1, "little")
            byte_b = (source_bytes[start_ind + 1]).to_bytes(1, "little")
            byte_c = (source_bytes[start_ind + 2]).to_bytes(1, "little")

            if byte_a + byte_b + byte_c == END_SYMBOL:
                break

            count_bytes.append(source_bytes[start_ind])
            start_ind += 1

        return start_ind + 3, count_bytes

    @staticmethod
    def _read_codes(source_bytes, start_ind):
        code_bytes = []
        while start_ind < len(source_bytes):
            code_bytes.append(source_bytes[start_ind].to_bytes(1, "little"))
            start_ind += 1

        return code_bytes

    @property
    def tree_bytes(self):
        return self.haffman_tree_bytes

    @property
    def code_bytes(self):
        return self.haffman_code_bytes

    @property
    def count_bytes(self):
        return self.count_in_bytes
