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
            # I'm kind of sorry for this, but not enough to change it
            # it is just getting the start and end of what locations are added
            # to this wire
            start, end = (lambda a: (a[0], a[1]) if a[0] < a[1] else (a[1], a[0]))((x, o_x) if x_mod else (y, o_y))

            for i in range(start, end):
                val = (i, y) if x_mod is True else (x, i)
                # this is preferable to having to make a class that inherits
                # from defaultdict and ordereddict
                instruction_set[instr_count].append(val)
                wire_locs.add(val)
            self.turns.add(self.current_loc)
            x_mod = False
            instr_count += 1

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
                    total_steps = v.index(loc)
                    for i in range(1, k):
                        total_steps += len(instruction_set[i])
                    step_list.append(total_steps)
                    break
        return step_list

    def print_grid(self):
        for w in self.wire_list:
            self.filled_locs.extend(list(w))

        x_sort = sorted(self.filled_locs, key=lambda a: a[0])
        min_x = x_sort[0][0]
        max_x = x_sort[-1][0]

        y_sort = sorted(self.filled_locs, key=lambda a: a[1])
        min_y = y_sort[0][1]
        max_y = y_sort[-1][1]

        with open("out", "w") as f:
            for y in range(max_y, min_y - 1, -1):
                for x in range(min_x, max_x + 1):
                    loc = (x, y)
                    if loc in self.filled_locs:
                        if loc in self.intersections:
                            f.write("i")
                        elif loc == (0, 0):
                            f.write("o")
                        else:
                            f.write("x")
                    else:
                        f.write(".")
                f.write("\n")


g = Grid()
with open("Day3In.txt", "r") as f:
    g.add_wire(f.readline())
    g.add_wire(f.readline())
g.count_intersections()
p1res = g.closest_intersection
p2res = g.steps_to_intersections[g.fewest_steps_to_intersection]
print(f"Part 1: {p1res}")
print(f"Part 2: {p2res}")
