import time

from queue import PriorityQueue

from .huffman_reader import SEPARATOR


class HuffmanNode(object):

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


class HuffmanTree(object):

    UP = b"U"
    DOWN = b"D"

    def __init__(self, param):
        """
        :param param: dict as freq of symbols or coded string
        """
        self.head = None
        self.haffman_leaves = dict()

        if issubclass(type(param), dict):
            freq = param
            self._build_by_freq(freq)
        else:
            code_str = param
            self._buid_by_bytes(code_str)

    def _build_by_freq(self, frequency):
        node_queue = PriorityQueue()
        for symbol in frequency:
            node = HuffmanNode(frequency[symbol], symbol)
            self.haffman_leaves[symbol] = node
            node_queue.put(node)

        while node_queue.qsize() != 1:
            node_a = node_queue.get()
            node_b = node_queue.get()
            parent = HuffmanNode(node_a.count + node_b.count, node_a.symbol + node_b.symbol)
            parent.left_child = node_a
            parent.right_child = node_b
            node_a.parent = parent
            node_b.parent = parent

            node_queue.put(parent)
            self.head = parent

    def _buid_by_bytes(self, tree_bytes):
        self.head = HuffmanNode(-1, None)

        next_node = self.head
        found_command = False
        byte_symbol = b""
        for byte in tree_bytes:
            if found_command:
                if byte == SEPARATOR:
                    next_node.symbol = byte_symbol.decode("cp1251")
                    byte_symbol = b""
                    found_command = False
                else:
                    byte_symbol += byte
            else:
                if byte == HuffmanTree.DOWN:
                    new_node = HuffmanNode(-1, None, next_node)
                    if next_node.left_child is None:
                        next_node.left_child = new_node
                    else:
                        next_node.right_child = new_node
                    next_node = new_node
                else:
                    next_node = next_node.parent
                    while next_node.right_child is not None and next_node.parent is not None:
                        next_node = next_node.parent

                    new_node = HuffmanNode(-1, None, next_node)
                    next_node.right_child = new_node
                    next_node = new_node
                found_command = True

    @property
    def leaves(self):
        return self.haffman_leaves

    def tree_code(self):
        coded_tree_str = b""
        prev_node = None

        start = time.time()
        for node in self.dfs():
            if prev_node is None:
                prev_node = node
                continue
            # move left
            if prev_node.left_child is not None and prev_node.left_child == node:
                coded_tree_str += b"D"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="cp1251")
                coded_tree_str += SEPARATOR
            # move right
            elif prev_node.right_child is not None and prev_node.right_child == node:
                coded_tree_str += b"D"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="cp1251")
                coded_tree_str += SEPARATOR
            # move up
            else:
                coded_tree_str += b"U"
                if node.is_leaf():
                    coded_tree_str += bytes(node.symbol, encoding="cp1251")
                coded_tree_str += SEPARATOR

            prev_node = node

        end = time.time()
        print(f"Tree was decoded: {end - start}")
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
