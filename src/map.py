import math
from graph import Graph

class Map(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._data = []

        for i in range(height):
            self._data.append([0] * width)

        v = int(math.ceil(width / 2.0))

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

    def is_walkable(self, x, y):
        return self[y][x] == 0

    def find_path(self, from_, to):
        return self._graph.search(from_, to)

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