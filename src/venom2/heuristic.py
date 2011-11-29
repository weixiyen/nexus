from math import sqrt

def manhatton(start, end):
    """Returns the Manhattan distance."""

    x1, y1 = start
    x2, y2 = end

    return abs(x2 - x1) + abs(y2 - y1)

def diagonal(start, end):
    """Returns the Chebyshev distance."""

    x1, y1 = start
    x2, y2 = end

    return max(abs(x2 - x1), abs(y2 - y1))

def euclidean(start, end):
    """Returns the Euclidean distance."""

    dx = end[0] - start[0]
    dy = end[1] - start[1]

    return sqrt(dx * dx + dy * dy)

