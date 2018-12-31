class HaffmanTable(object):

    def __init__(self, haffman_leaves):
        """
        :param haffman_leaves: dict with HaffmanTree leaves
        """
        self.haffman_codes = dict()
        self.haffman_leaves = haffman_leaves
        self._build()

    def _build(self):
        for symbol in self.haffman_leaves:
            haffman_node = self.haffman_leaves[symbol]
            self.haffman_codes[symbol] = ""
            prev_node = haffman_node
            while prev_node.parent is not None:
                next_node = prev_node.parent
                if next_node.left_child == prev_node:
                    self.haffman_codes[haffman_node.symbol] = \
                        '0' + self.haffman_codes[symbol]
                else:
                    self.haffman_codes[haffman_node.symbol] = \
                        '1' + self.haffman_codes[symbol]
                prev_node = next_node

    def __getitem__(self, symbol):
        return self.haffman_code(symbol)

    def __contains__(self, symbol):
        return symbol in self.haffman_codes

    def haffman_code(self, symbol):
        if symbol in self.haffman_codes:
            return self.haffman_codes[symbol]
        raise ValueError(f"Symbol: {symbol} is not a key of dict")
