#import time
#import random
#from map import Map
#from astar import astar
#
## MAIN
#dirs = 8 # number of possible directions to move on the map
#if dirs == 4:
#    dx = [1, 0, -1, 0]
#    dy = [0, 1, 0, -1]
#else:
#    dx = [1, 1, 0, -1, -1, -1, 0, 1]
#    dy = [0, 1, 1, 1, 0, -1, -1, -1]
#
#
#_m = Map(30, 30)
#
## randomly select start and finish locations from a list
#sf = [
#    (0, 0, _m.height - 1, _m.width - 1),
#    (0, _m.width - 1, _m.height - 1, 0),
#    (_m.height / 2 - 1, _m.width / 2 - 1, _m.height / 2 + 1, _m.width / 2 + 1),
#    (_m.height / 2 - 1, _m.width / 2 + 1, _m.height / 2 + 1, _m.width / 2 - 1),
#    (_m.height / 2 - 1, 0, _m.height / 2 + 1, _m.width - 1),
#    (_m.height / 2 + 1, _m.width - 1, _m.height / 2 - 1, 0),
#    (0, _m.width / 2 - 1, _m.height - 1, _m.width / 2 + 1),
#    (_m.height - 1, _m.width / 2 + 1, 0, _m.width / 2 - 1)
#]
#
#(xa, ya, xb, yb) = random.choice(sf)
#
#print 'Map size (X,Y): ', _m.width, _m.height
#print 'Start: ', xa, ya
#print 'Finish: ', xb, yb
#t = time.time()
#route = astar(_m, _m.height, _m.width, dirs, dx, dy, xa, ya, xb, yb)
#print 'Time to generate the route (seconds): ', time.time() - t
#print 'Route:'
#print route
#
## mark the route on the map
#if len(route) > 0:
#    x = xa
#    y = ya
#    _m[y][x] = 2
#    for i in range(len(route)):
#        j = int(route[i])
#        x += dx[j]
#        y += dy[j]
#        _m[y][x] = 3
#    _m[y][x] = 4
#
## display the map with the route added
#print 'Map:'
#for y in range(_m.width):
#    for x in range(_m.height):
#        xy = _m[y][x]
#        if not xy:
#            print '.', # space
#        elif xy == 1:
#            print 'O', # obstacle
#        elif xy == 2:
#            print 'S', # start
#        elif xy == 3:
#            print 'R', # route
#        elif xy == 4:
#            print 'F', # finish
#    print

from game import Game
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

game = Game()
game.spawn('Lizard')
game.spawn('Lizard')
game.spawn('Lizard')
game.spawn('Lizard')
game.spawn('Lizard')
game.spawn('Lizard')

for entity in game.entities:
    logging.debug(list(entity.nearby()))