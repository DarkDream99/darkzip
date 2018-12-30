from queue import PriorityQueue


class HaffmanNode(object):

    def __init__(self, count, symbol, parent=None):
        self.count = count
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.symbol = symbol

    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        if other is None:
            return False
        return self.symbol == other.symbol

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)


class HaffmanTree(object):

    def __init__(self, freq):
        """
        :param freq: dict
        """
        self.frequency = freq
        self.head = None
        self.haffman_leaves = dict()
        self._build()

    def _build(self):
        node_queue = PriorityQueue()
        for symbol in self.frequency:
            node = HaffmanNode(self.frequency[symbol], symbol)
            self.haffman_leaves[symbol] = node
            node_queue.put(node)

        while node_queue.qsize() != 1:
            node_a = node_queue.get()
            node_b = node_queue.get()
            parent = HaffmanNode(node_a.count + node_b.count, node_a.symbol + node_b.symbol)
            parent.left_child = node_a
            parent.right_child = node_b
            node_a.parent = parent
            node_b.parent = parent

            node_queue.put(parent)
            self.head = parent

    @property
    def leaves(self):
        return self.haffman_leaves

    def DFS(self):
        selected_nodes = []
        colors = ['w'] * len(self.frequency)

        pass
