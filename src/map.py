import math
from graph import Graph

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._data = []

        for i in range(height):
            self._data.append([0] * width)

        for x in range(height / 8, height * 7 / 8):
            self._data[width / 2][x] = 1

        for y in range(width/8, width * 7 / 8):
            self._data[y][height / 2] = 1

        self.graph = Graph(self)

    def is_walkable(self, x, y):
        return self[y][x] == 0

    def find_path(self, from_, to):
        return self.graph.search(from_, to)

    @staticmethod
    def get_distance(from_, to):
        if not isinstance(from_, (list, tuple)):
            from_ = (from_.x, from_.y)

        if not isinstance(to, (list, tuple)):
            to = (to.x, to.y)

        xd = to[0] - from_[0]
        yd = to[1] - from_[1]

        return math.sqrt(xd * xd + yd * yd)

    def __getitem__(self, item):
        return self._data[item]

    def serialize(self):
        return self._data