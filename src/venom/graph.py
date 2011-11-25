from heapq import heappop, heappush
from collections import defaultdict
from venom import heuristic

DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

class Node(object):
    def __init__(self, graph, x, y, type_):
        self.graph = graph
        self.data = {}
        self.x = x
        self.y = y
        self.position = (x, y)
        self.type = type_

    def is_walkable(self):
        """Return True if current node is empty."""

        return not self.type

    def get_neigbhors(self, walkable_only=True):
        """Returns neighbors of current node."""

        neigbhors = []

        x = self.x
        y = self.y

        for dx, dy in DIRECTIONS:
            node = self.graph.get_node(x + dx, y + dy)

            if node is None:
                continue

            if walkable_only and not node.is_walkable():
                continue

            neigbhors.append(node)

        return neigbhors

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
        """Returns node at (x,y)"""

        if (0 <= x < self.grid.width) and (0 <= y < self.grid.height):
            try:
                return self.nodes[y][x]
            except IndexError:
                pass

        return None

    def search(self, start, end, walkable_only=True, heuristic=heuristic.euclidean):
        """Performs the A* algorithm from start to end on the current graph.
        If walkable_only is False then collisions are not considered.
        """

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

        heap = []
        heappush(heap, (f[start], start))

        while heap:
            _, current_node = heappop(heap)

            if current_node == end:
                path = []

                while parent[current_node]:
                    path.append([current_node.x, current_node.y])
                    current_node = parent[current_node]

                return path

            closed[current_node] = True

            for neighbor in current_node.get_neigbhors(walkable_only):
                if closed[neighbor]:
                    continue

                g_score = g[current_node] + 1
                been_visited = visited[neighbor]

                if not been_visited or g_score < g[neighbor]:
                    h_score = h[neighbor] or heuristic(neighbor.position, end.position)

                    visited[neighbor] = True
                    parent[neighbor] = current_node
                    h[neighbor] = h_score
                    g[neighbor] = g_score
                    f[neighbor] = f_score = g_score + h_score

                    if been_visited:
                        heap = [(score, node) for score, node in heap if node != neighbor]

                    heappush(heap, (f_score, neighbor))

        return []