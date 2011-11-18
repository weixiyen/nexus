from heapq import heappush, heappop
import math

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
        xd = x - self.x
        yd = y - self.y
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return d

# A-star algorithm.
# The path returned will be a string of digits of directions.
def astar(test_map, dirs, dx, dy, xa, ya, xb, yb):
    m = test_map.width
    n = test_map.height

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
    n0 = Node(xa, ya, 0, 0)
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
                    or test_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):

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