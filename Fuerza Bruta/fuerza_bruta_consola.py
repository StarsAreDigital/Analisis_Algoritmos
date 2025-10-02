import random
import math

N = 5
MIN_POINT = 0
MAX_POINT = 40

class Point:
    x = 0
    y = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

def dist(a: Point, b: Point):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.sqrt(dx * dx + dy * dy)


def distances(index: int, points: list[Point]):
    if index < 0 or index >= len(points):
        raise IndexError("Index out of range")
    return [dist(point, points[index]) for point in points]


def closest_point(index: int, points: list[Point]):
    min_point = points[index]
    min_dist = float("Inf")
    for i, point in enumerate(points):
        if i == index:
            continue
        d = dist(point, points[index])
        if d < min_dist:
            min_point = point
            min_dist = d
    return min_point


def lerp(low: float, high: float, t: float):
    return low + (high - low) * t


def find_closest_points(points: list[Point]):
    min_dist = float("Inf")
    indexes = (None, None)
    for i, a in enumerate(points, 1):
        for j, b in enumerate(points, 1):
            if i >= j:
                continue
            d = dist(a, b)
            if d < min_dist:
                min_dist = d
                indexes = (i, j)
    return indexes


points = [
    Point(random.randint(MIN_POINT, MAX_POINT), random.randint(MIN_POINT, MAX_POINT))
    for _ in range(N)
]

print("Los puntos son:")
for i, point in enumerate(points, 1):
    print(f"P{i}: ({point.x}, {point.y})")

closest = find_closest_points(points)
a, b = points[closest[0] - 1], points[closest[1] - 1]
print(f"Los puntos mas cercanos son P{closest[0]} a P{closest[1]} (d = {dist(a, b)})")
