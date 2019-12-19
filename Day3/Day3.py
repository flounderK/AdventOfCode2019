#!/usr/bin/python
import re
from collections import defaultdict


class Grid(object):
    def __init__(self):
        self.filled_locs = list()
        self.intersections = set()
        self.current_loc = (0, 0)
        self.closest_intersection = 0
        self.wire_list = list()
        self.turns = set()
        self.instruction_sets = list()
        self.steps_to_intersections = dict()

    def add_wire(self, vector_list):
        if isinstance(vector_list, str):
            vector_list = [i.strip() for i in vector_list.split(",")]

        rexp = re.compile(r'([LUDR])(\d+)')
        x_mod = False
        wire_locs = set()
        instruction_set = defaultdict(list)
        instr_count = 1
        last_dir = None
        # convert the numeric characters to integers
        for direction, amount in map(lambda a: (a[0], int(a[1])),
                                     [re.match(rexp, i).groups() for i in vector_list]):
            x, y = o_x, o_y = self.current_loc
            if direction == 'D':
                y -= amount
            elif direction == 'U':
                y += amount
            elif direction == 'L':
                x -= amount
                x_mod = True
            elif direction == 'R':
                x += amount
                x_mod = True

            self.current_loc = (x, y)
            self.turns.add(self.current_loc)
            # I'm kind of sorry for this, but not enough to change it
            # it is just getting the start and end of what locations are added
            # to this wire
            start, end = (lambda a: (a[0], a[1]) if a[0] < a[1] else (a[1], a[0]))((x, o_x) if x_mod else (y, o_y))
            extra_end = 1 if (last_dir, direction) == ("U", "L") else 0
            extra_end += 1 if (last_dir, direction) == ("R", "D") else 0
            for i in range(start, end + extra_end):
                val = (i, y) if x_mod is True else (x, i)
                # don't include (0, 0) because it is never stepped to,
                # only from
                if val != (0, 0):
                    # using ints is preferable to having to make a class that
                    # inherits from defaultdict and ordereddict
                    # check to make sure a turn doesn't get added twice
                    # because locations are not always put in in numeric order
                    if val not in instruction_set[instr_count - 1]:
                        instruction_set[instr_count].append(val)
                    wire_locs.add(val)

            # reverse list so that locations occur in correct order
            # for counting the number of steps it has taken
            if direction == 'L' or direction == 'D':
                instruction_set[instr_count].reverse()
            x_mod = False
            instr_count += 1
            last_dir = direction

        self.current_loc = (0, 0)
        self.wire_list.append(wire_locs)
        self.instruction_sets.append(instruction_set)

    def count_intersections(self):
        for w1 in self.wire_list:
            for w2 in self.wire_list:
                if w1 == w2:
                    continue
                new_inx = w1.intersection(w2)
                self.intersections = self.intersections.union(new_inx)
        if (0, 0) in self.intersections:
            self.intersections.remove((0, 0))

        self.intersections = self.intersections - self.turns
        self.closest_intersection = sorted([abs(x) + abs(y) for x, y in self.intersections])[0]
        for inx in self.intersections:
            self.steps_to_intersections[inx] = sum(self.get_steps_to_loc(inx))

        self.fewest_steps_to_intersection = sorted([k for k in self.steps_to_intersections.keys()],
                                                   key=lambda k: self.steps_to_intersections[k])[0]

    def get_steps_to_loc(self, loc):
        """return a list of the number of steps required to get to a given location"""
        step_list = list()
        for instruction_set in self.instruction_sets:
            for k, v in instruction_set.items():
                if loc in v:
                    total_steps = v.index(loc) + 1
                    # go through every directional line before the current one
                    # and get the total number of items
                    for i in range(1, k):
                        total_steps += len(instruction_set[i])
                    step_list.append(total_steps)
                    break
        return step_list

    def print_grid(self, filename="out"):
        for w in self.wire_list:
            self.filled_locs.extend(list(w))

        x_sort = sorted(self.filled_locs, key=lambda a: a[0])
        min_x = x_sort[0][0]
        max_x = x_sort[-1][0]

        y_sort = sorted(self.filled_locs, key=lambda a: a[1])
        min_y = y_sort[0][1]
        max_y = y_sort[-1][1]

        with open(filename, "w") as f:
            for y in range(max_y, min_y - 1, -1):
                for x in range(min_x, max_x + 1):
                    loc = (x, y)
                    if loc in self.filled_locs:
                        if loc in self.intersections:
                            f.write("i")
                        elif loc == (0, 0):
                            f.write("o")
                        elif loc in self.turns:
                            f.write("+")
                        else:
                            f.write("x")
                    elif loc == (0, 0):
                        f.write("o")
                    else:
                        f.write(".")
                f.write("\n")


# test_sets = [["R8,U5,L5,D3", "U7,R6,D4,L4", 6, 30],
#              ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
#               "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, 410],
#              ["R75,D30,R83,U83,L12,D49,R71,U7,L72",
#               "U62,R66,U55,R34,D71,R55,D58,R83", 159, 610]]
#
# for w1, w2, a1, a2 in test_sets:
#     print("Starting new test")
#     g = Grid()
#     g.add_wire(w1)
#     g.add_wire(w2)
#     g.count_intersections()
#     res1 = g.closest_intersection
#     res2 = g.steps_to_intersections[g.fewest_steps_to_intersection]
#     try:
#         assert res1 == a1
#     except:
#         print(f"{res1} != {a1}")
#
#     try:
#         assert res2 == a2
#     except:
#         print(f"{res2} != {a2}")
#         g.print_grid()
#         break

g = Grid()
with open("Day3In.txt", "r") as f:
    g.add_wire(f.readline())
    g.add_wire(f.readline())
g.count_intersections()
p1res = g.closest_intersection
p2res = g.steps_to_intersections[g.fewest_steps_to_intersection]
print(f"Part 1: {p1res}")
print(f"Part 2: {p2res}")
