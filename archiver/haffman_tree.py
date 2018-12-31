from queue import PriorityQueue

from .haffman_reader import SEPARATOR


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

    def __contains__(self, other_node):
        return self.symbol.find(other_node.symbol) != -1

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

    def tree_code(self):
        coded_tree_str = b""
        prev_node = None

        is_upping = False
        for node in self.dfs():
            if prev_node is None:
                prev_node = node
                continue
            # move left
            if prev_node.left_child is not None and prev_node.left_child == node:
                coded_tree_str += b"D"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="utf-8")
                coded_tree_str += SEPARATOR
            # move right
            elif prev_node.right_child is not None and prev_node.right_child == node:
                coded_tree_str += b"D"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="utf-8")
                coded_tree_str += SEPARATOR
            # move up
            else:
                coded_tree_str += b"U"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="utf-8")
                coded_tree_str += SEPARATOR

            prev_node = node

        return coded_tree_str

    def dfs(self):
        selected_nodes = [self.head]
        used_nodes_symbols = set()
        used_nodes_symbols.add(self.head.symbol)

        while len(selected_nodes) != 0:
            node = selected_nodes.pop()
            yield node

            next_node = node.right_child
            if next_node is not None and next_node.symbol not in used_nodes_symbols:
                used_nodes_symbols.add(next_node.symbol)
                selected_nodes.append(next_node)
            next_node = node.left_child
            if next_node is not None and next_node.symbol not in used_nodes_symbols:
                used_nodes_symbols.add(next_node.symbol)
                selected_nodes.append(next_node)

