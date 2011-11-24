from math import sqrt, ceil
from graph import Graph

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._data = []

        for i in range(height):
            self._data.append([0] * width)

        v = int(ceil(width / 2.0))

        for y in xrange(v):
            for x in xrange(v):
                x = v - y - x

                if x < 0:
                    break

                self._data[y][x] = 1
                self._data[-y][x] = 1
                self._data[y][-x] = 1
                self._data[-y][-x] = 1

        self._graph = Graph(self)

        self.find_path = self._graph.search

    def block(self, x, y, width=1, height=1):
        width = int(ceil(width / 32.0 / 2.0))
        height = int(ceil(height / 16.0 / 2.0))

        for i in xrange(height):
            for j in xrange(width):
                node = self._graph.get_node(x + j, y - i)

                if not node:
                    continue

                node.type = 2
                self._data[y - i][x + j] = 2

            for j in xrange(width):
                node = self._graph.get_node(x - j, y - i)

                if not node:
                    continue

                node.type = 2
                self._data[y - i][x - j] = 2

    def is_walkable(self, x, y):
        return self[y][x] == 0

    def get_positions(self, x, y, radius=1):
        nodes = []

        def add_node(node):
            if node in nodes or self.get_distance((x, y), node.pos) > radius:
                return

            nodes.append(node)
            map(add_node, node.get_neigbhors())

        add_node(self._graph.get_node(x, y))

        return [node.pos for node in nodes]

    @staticmethod
    def get_distance(from_, to):
        dx = to[0] - from_[0]
        dy = to[1] - from_[1]
        return sqrt(dx * dx + dy * dy)

    def __getitem__(self, item):
        return self._data[item]

    def serialize(self):
        return self._data