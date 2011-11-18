import math
import functools
from heapq import heappush, heappop

class memoized(object):
    """
    Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __copy__(self):
        """
        Don't copy the cache in a copy.
        """
        return memoized(self.func)
    def __deepcopy__(self, memo):
        """
        Don't copy the cache in a deep copy.
        """
        return memoized(self.func)

    def __call__(self, *args):
       try:
           return self.cache[args]
       except KeyError:
           value = self.func(*args)
           self.cache[args] = value
           return value
       except TypeError:
           # uncachable -- for instance, passing a list as an argument.
           # Better to not cache than to blow up entirely.
           return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
    def clear_cache(self):
        self.cache = {}

class Node(object):
    def __init__(self, x=0, y=0, distance=0, priority=0):
        self.x = x # x position
        self.y = y # y position
        self.distance = distance  # total distance already travelled to reach the node
        self.priority = priority # priority = distance + remaining distance estimate

    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority

    def update_priority(self, x, y):
        self.priority = self.distance + self.estimate(x, y) * 10 # A*

    # give higher priority to going straight instead of diagonally
    def next_move(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10

    # Estimation function for the remaining distance to the goal.
    def estimate(self, x, y):
        return Map.get_distance([x, y], [self.x, self.y])

class Map(object):
    DX = [1, 1, 0, -1, -1, -1, 0, 1]
    DY = [0, 1, 1, 1, 0, -1, -1, -1]

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
        return self[y][x] == 1

    @memoized
    def find_route(self, from_, to):
        dx = Map.DX
        dy = Map.DY
        dirs = 8

        xa, ya = from_
        xb, yb = to

        m = self.width
        n = self.height

        closed_nodes_map = [] # map of closed (tried-out) nodes
        open_nodes_map = [] # map of open (not-yet-tried) nodes
        dir_map = [] # map of dirs

        row = [0] * n

        for i in range(m): # create 2d arrays
            closed_nodes_map.append(list(row))
            open_nodes_map.append(list(row))
            dir_map.append(list(row))

        pq = [[], []] # priority queues of open (not-yet-tried) nodes
        pqi = 0 # priority queue index

        # create the start node and push into list of open nodes
        n0 = Node(xa, ya)
        n0.update_priority(xb, yb)
        heappush(pq[pqi], n0)
        open_nodes_map[ya][xa] = n0.priority # mark it on the open nodes map

        # A* search
        while len(pq[pqi]) > 0:
            # get the current node w/ the highest priority
            # from the list of open nodes
            n1 = pq[pqi][0] # top node
            n0 = Node(n1.x, n1.y, n1.distance, n1.priority)
            x = n0.x
            y = n0.y
            heappop(pq[pqi]) # remove the node from the open list
            open_nodes_map[y][x] = 0
            closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

            # quit searching when the goal is reached
            # if n0.estimate(xB, yB) == 0:
            if x == xb and y == yb:
                # generate the path from finish to start
                # by following the dirs
                path = []

                while not (x == xa and y == ya):
                    j = dir_map[y][x]
                    c = str((j + dirs / 2) % dirs)
                    path.insert(0, int(c))
                    x += dx[j]
                    y += dy[j]

                return path

            # generate moves (child nodes) in all possible dirs
            for i in range(dirs):
                xdx = x + dx[i]
                ydy = y + dy[i]

                if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                        or self.is_obstacle(xdx, ydy) == 1 or closed_nodes_map[ydy][xdx] == 1):

                    # generate a child node
                    m0 = Node(xdx, ydy, n0.distance, n0.priority)
                    m0.next_move(dirs, i)
                    m0.update_priority(xb, yb)

                    # if it is not in the open list then add into that
                    if not open_nodes_map[ydy][xdx]:
                        open_nodes_map[ydy][xdx] = m0.priority
                        heappush(pq[pqi], m0)
                        # mark its parent node direction
                        dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    elif open_nodes_map[ydy][xdx] > m0.priority:
                        # update the priority
                        open_nodes_map[ydy][xdx] = m0.priority
                        # update the parent direction
                        dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                        # replace the node
                        # by emptying one pq to the other one
                        # except the node to be replaced will be ignored
                        # and the new node will be pushed in instead
                        while not (pq[pqi][0].x == xdx and pq[pqi][0].y == ydy):
                            heappush(pq[1 - pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        heappop(pq[pqi]) # remove the target node
                        # empty the larger size priority queue to the smaller one
                        if len(pq[pqi]) > len(pq[1 - pqi]):
                            pqi = 1 - pqi
                        while len(pq[pqi]) > 0:
                            heappush(pq[1-pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        pqi = 1 - pqi
                        heappush(pq[pqi], m0) # add the better node instead

        return [] # if no route found

    def get_delta(self, move):
        return Map.DX[move], Map.DY[move]

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