from heapq import heappop, heappush
from collections import defaultdict

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

    def is_walkable(self):
        return self.type == 0

    def get_neigbhors(self, walkable_only=True):
        ret = []

        x = self.x
        y = self.y

        for i in range(8):
            x2 = x + DX[i]
            y2 = y + DY[i]

            if x2 < 0 or y2 < 0:
                continue

            node = self.graph.get_node(x + DX[i], y + DY[i])

            if node is None:
                continue

            if walkable_only and not node.is_walkable():
                continue

            ret.append(node)

        return ret

class Graph(object):
    def __init__(self, grid):
        self.grid = grid
        self.nodes = []

        for y, row in enumerate(grid):
            nodes = []

            for x, type_ in enumerate(row):
                nodes.append(Node(self, x, y, type_))

            self.nodes.append(nodes)

    def __iter__(self):
        return self.nodes.__iter__()

    def get_node(self, x, y):
        if (0 <= x < self.grid.width) and (0 <= y < self.grid.height):
            try:
                return self.nodes[y][x]
            except IndexError:
                pass

        return None

    def search(self, start, end, walkable_only=True, heuristic=manhatton):
        start = self.get_node(*start)
        end = self.get_node(*end)

        if not start or not end or not end.is_walkable():
            return []

        f = defaultdict(lambda: 0)
        g = defaultdict(lambda: 0)
        h = defaultdict(lambda: 0)
        visited = defaultdict(lambda: False)
        closed = defaultdict(lambda: False)
        parent = defaultdict(lambda: None)

        open_heap = []
        heappush(open_heap, (f[start], start))

        while open_heap:
            _, current_node = heappop(open_heap)

            if current_node == end:
                ret = []

                while parent[current_node]:
                    ret.append([current_node.x, current_node.y])
                    current_node = parent[current_node]

                return ret

            closed[current_node] = True

            for neighbor in current_node.get_neigbhors(walkable_only):
                if closed[neighbor]:
                    continue

                g_score = g[current_node] + 1
                been_visited = visited[neighbor]

                if not been_visited or g_score < g[neighbor]:
                    visited[neighbor] = True
                    parent[neighbor] = current_node
                    h[neighbor] = h[neighbor] or heuristic(neighbor.pos, end.pos)
                    g[neighbor] = g_score
                    f[neighbor] = g[neighbor] + h[neighbor]

                    if been_visited:
                        open_heap =  [(score, value) for score, value in open_heap if value != neighbor]

                    heappush(open_heap, (f[neighbor], neighbor))

        return []