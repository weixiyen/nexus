from math import ceil
from random import randint
from venom.graph import Graph
from venom.heuristic import euclidean

EMPTY = 0
BLANK = 1
OBJECT = 2

class Map(object):
    def __init__(self, width, height, scale=32):
        self.width = width
        self.height = height
        self.scale = scale

        self._grid = []

        for i in range(height):
            self._grid.append([0] * width)

        v = int(ceil(width / 2.0))

        for y in xrange(v):
            for x in xrange(v):
                x = v - y - x

                if x < 0:
                    break

                self._grid[y][x] = BLANK
                self._grid[y][-x] = BLANK
                self._grid[-y][x] = BLANK
                self._grid[-y][-x] = BLANK

        self._graph = Graph(self)

        self.find_path = self._graph.search

    def __getitem__(self, item):
        return self._grid[item]

    def add_collision(self, x, y, width=1, height=1):
        """Add collisions to the grid originating from the bottom center of (x,y)."""

        width = int(ceil(width / (self.scale * 1.0) / 1.8))
        height = int(ceil(height / (self.scale * 0.5)))

        graph = self._graph

        for i in xrange(height):
            for j in xrange(width):
                for node in [graph.get_node(x - j, y - i), graph.get_node(x + j, y - i)]:
                    if not node:
                        continue

                    node.type = self._grid[node.y][node.x] = OBJECT

    def is_walkable(self, x, y):
        """Returns whether or not (x,y) is empty."""

        return self[y][x] == EMPTY

    def get_random_position(self):
        while True:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)

            if self.is_walkable(x, y):
                return x, y

    def get_points_in_radius(self, x, y, radius=1):
        """Returns all possible points within a radius originating from (x,y)."""

        nodes = []

        def add_node(node):
            if node in nodes or self.distance((x, y), node.position) > radius:
                return

            nodes.append(node)
            map(add_node, node.get_neigbhors())

        add_node(self._graph.get_node(x, y))

        return [node.position for node in nodes]

    @staticmethod
    def distance(start, end):
        """Returns the Euclidean distance."""
        return euclidean(start, end)

    def serialize(self):
        return self._grid