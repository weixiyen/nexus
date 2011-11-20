from heapq import heappop, heappush

DX = [1, 1, 0, -1, -1, -1, 0, 1]
DY = [0, 1, 1, 1, 0, -1, -1, -1]

def manhatton(start, end):
    x1, y1 = start
    x2, y2 = end

    return abs(x2 - x1) + abs(y2 - y1)

class Node(object):
    def __init__(self, graph, x, y, type_):
        self.graph = graph
        self.data = {}
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.type = type_

        self.f = 0
        self.g = 0
        self.h = 0
        self.visited = False
        self.closed = False
        self.parent = None

    def is_walkable(self):
        return self.type == 0

    def get_neigbhors(self):
        ret = []

        x = self.x
        y = self.y

        for i in range(8):
            x2 = x + DX[i]
            y2 = y + DY[i]

            if x2 < 0 or y2 < 0:
                continue

            try:
                node = self.graph.get_node(x + DX[i], y + DY[i])
            except IndexError:
                continue

            if not node.is_walkable():
                continue

            ret.append(node)

        return ret

    def get_heap_value(self):
        return self.f, self

class Graph(object):
    def __init__(self, grid):
        self.elements = grid
        self.nodes = []

        for y, row in enumerate(grid):
            nodes = []

            for x, type_ in enumerate(row):
                nodes.append(Node(self, x, y, type_))

            self.nodes.append(nodes)

    def __iter__(self):
        return self.nodes.__iter__()

    def get_node(self, x, y):
        return self.nodes[y][x]

    def search(self, start, end, heuristic=manhatton):
        for row in self.nodes:
            for node in row:
                node.f = 0
                node.g = 0
                node.h = 0
                node.visited = False
                node.closed = False
                node.parent = None

        start = self.get_node(*start)
        end = self.get_node(*end)

        open_heap = []
        heappush(open_heap, start.get_heap_value())

        while open_heap:
            _, current_node = heappop(open_heap)

            if current_node == end:
                ret = []

                while current_node.parent:
                    ret.append([current_node.x, current_node.y])
                    current_node = current_node.parent

                return ret

            current_node.closed = True

            for neighbor in current_node.get_neigbhors():
                if neighbor.closed:
                    continue

                g_score = current_node.g + 1
                been_visited = neighbor.visited

                if not been_visited or g_score < neighbor.g:
                    neighbor.visited = True
                    neighbor.parent = current_node
                    neighbor.h = neighbor.h or heuristic(neighbor.pos, end.pos)
                    neighbor.g = g_score
                    neighbor.f = neighbor.g + neighbor.h

                    if been_visited:
                        open_heap =  [(score, value) for score, value in open_heap if value != neighbor]

                    heappush(open_heap, neighbor.get_heap_value())

        return []