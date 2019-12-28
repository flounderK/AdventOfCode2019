#!/usr/bin/python
from collections import defaultdict, OrderedDict
import string
import math


class Grid(object):
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        if isinstance(self.raw_grid, str):
            self.raw_grid = self.raw_grid.split()

        self.filled_locations = list()
        self.asteroid_visibility_map = dict()
        self.asteroid_slope_map = dict()
        self.asteroid_degree_map = dict()
        self.asteroid_visibility_map_degrees = dict()
        self.find_asteroids()
        self.map_asteroid_visibility()

    def find_asteroids(self):
        for r_i, r in enumerate(self.raw_grid):
            for c_i, c in enumerate(r):
                if c == '#':
                    self.filled_locations.append((c_i, r_i))

    def map_asteroid_visibility(self):
        for i in self.filled_locations:
            slope_map = self.map_asteroid_LOS(i)
            degree_map = self.map_asteroid_LOS_degrees(i)
            self.asteroid_visibility_map[i] = len(slope_map.keys())
            self.asteroid_visibility_map_degrees[i] = len(degree_map.keys())
            self.asteroid_slope_map[i] = slope_map
            self.asteroid_degree_map[i] = degree_map

    def map_asteroid_LOS(self, location):
        x, y = location
        slope_map = defaultdict(list)
        for x1, y1 in self.filled_locations:
            if x1 == x and y1 == y:
                continue
            # calculate slope
            dx = x - x1
            dy = y - y1
            if dx == 0:
                m = "y"
                m += "u" if y < y1 else "d"
            elif dy == 0:
                m = "x"
                m += "l" if x > x1 else "r"
            else:
                m = str(dy / dx)
                m += "l" if x > x1 else "r"
            slope_map[m].append((x1, y1))

        return slope_map

    def map_asteroid_LOS_degrees(self, location):
        x, y = location
        degree_map = defaultdict(list)
        for x1, y1 in self.filled_locations:
            if x1 == x and y1 == y:
                continue
            # calculate slope
            dx = x - x1
            dy = y - y1
            if dx == 0:
                a = "y"
                v = 270
                b = "u" if y < y1 else "d"
            elif dy == 0:
                a = "x"
                v = 0
                b = "l" if x > x1 else "r"
            else:
                v = math.atan(dy / dx)
                b = "l" if x > x1 else "r"
            if b in ['d', 'r']:
                v = abs(v - 180)

            # Adjust to 0 degrees being directly up
            v -= 90
            if v < 0:
                v = 360 + v

            degree_map[v].append((x1, y1))

        return degree_map

    def print_grid_for_loc(self, location):
        slopes = [(i, s) for i, s in enumerate(self.asteroid_slope_map[location].items())]
        for i_y, y in enumerate(self.raw_grid):
            line = y
            for i_x, x in enumerate(y):
                for i, asm in slopes:
                    m, locs = asm
                    if (i_x, i_y) in locs:
                        c = i % len(string.ascii_letters)
                        line = line[:i_x] + string.ascii_letters[c] + line[i_x + 1:]
                        break
            print(line)


with open("Day10In.txt", "r") as f:
    content = [i for i in f.read().split()]

g = Grid(content)
station_position, p1res = sorted(g.asteroid_visibility_map.items(),
                                 key=lambda a: a[1],
                                 reverse=True)[0]

print(f"Part 1: {p1res}")

degree_map = g.asteroid_degree_map[station_position]
laser_vaporization_guide = list()
degrees_of_impact = sorted(degree_map.keys())
x, y = station_position
for degree in degrees_of_impact:
    lst = sorted(degree_map[degree],
                 key=lambda a: abs(x - a[0]) + abs(y - a[1]),
                 reverse=True)
    laser_vaporization_guide.append(lst)

count = 0
target_num = 200
while count < target_num:
    for v in laser_vaporization_guide:
        if len(v) == 0:
            continue
        loc = v.pop()
        count += 1
        if count == target_num:
            break

x1, y1 = loc
p2res = (x1 * 100) + y1
print(f"Part 2: {p2res}")

