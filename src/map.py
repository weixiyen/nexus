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

    def is_obstacle(self, x, y):
        return self[x][y] == 1

    def __getitem__(self, item):
        return self._data[item]