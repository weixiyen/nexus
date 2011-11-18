from heapq import heappush, heappop
import math
import time
import random

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
def astar(test_map, n, m, dirs, dx, dy, xa, ya, xb, yb):
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
            path = ''

            while not (x == xa and y == ya):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
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

    return '' # if no route found

for _ in xrange(100):
    # MAIN
    dirs = 8 # number of possible directions to move on the map
    if dirs == 4:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
    else:
        dx = [1, 1, 0, -1, -1, -1, 0, 1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]

    n = 50 # horizontal size of the map
    m = 50 # vertical size of the map
    test_map = []
    row = [0] * n
    for i in range(m): # create empty map
        test_map.append(list(row))

    # fillout the map with a '+' pattern
    for x in range(n / 8, n * 7 / 8):
        test_map[m / 2][x] = 1
    for y in range(m/8, m * 7 / 8):
        test_map[y][n / 2] = 1

    # randomly select start and finish locations from a list
    sf = [
        (0, 0, n - 1, m - 1),
        (0, m - 1, n - 1, 0),
        (n / 2 - 1, m / 2 - 1, n / 2 + 1, m / 2 + 1),
        (n / 2 - 1, m / 2 + 1, n / 2 + 1, m / 2 - 1),
        (n / 2 - 1, 0, n / 2 + 1, m - 1),
        (n / 2 + 1, m - 1, n / 2 - 1, 0),
        (0, m / 2 - 1, n - 1, m / 2 + 1),
        (n - 1, m / 2 + 1, 0, m / 2 - 1)
    ]

    (xa, ya, xb, yb) = random.choice(sf)

    print 'Map size (X,Y): ', n, m
    print 'Start: ', xa, ya
    print 'Finish: ', xb, yb
    t = time.time()
    route = astar(test_map, n, m, dirs, dx, dy, xa, ya, xb, yb)
    print 'Time to generate the route (seconds): ', time.time() - t
    print 'Route:'
    print route

    # mark the route on the map
    if len(route) > 0:
        x = xa
        y = ya
        test_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            test_map[y][x] = 3
        test_map[y][x] = 4

    # display the map with the route added
    print 'Map:'
    for y in range(m):
        for x in range(n):
            xy = test_map[y][x]
            if not xy:
                print '.', # space
            elif xy == 1:
                print 'O', # obstacle
            elif xy == 2:
                print 'S', # start
            elif xy == 3:
                print 'R', # route
            elif xy == 4:
                print 'F', # finish
        print
