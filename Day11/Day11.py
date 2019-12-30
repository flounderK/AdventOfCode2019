#!/usr/bin/python
from itertools import permutations
from collections import deque
import logging


class LiberalList(list):
    def __init__(self, *args, default=None):
        self._default = default
        super(LiberalList, self).__init__(*args)

    def copy(self, *args):
        return LiberalList(super(LiberalList, self).copy(*args))

    def __alloc_as_needed(self, args):
        if isinstance(args, slice):
            ind = args.stop
        else:
            ind = args

        last_ind = len(self) - 1
        if last_ind < ind:
            to_add = ind - last_ind
            lst_to_add = [self._default] * to_add
            self.extend(lst_to_add)

    def __getitem__(self, *args):
        self.__alloc_as_needed(*args)
        return super(LiberalList, self).__getitem__(*args)

    def __setitem__(self, lvalue, rvalue):
        self.__alloc_as_needed(lvalue)
        args = lvalue, rvalue
        return super(LiberalList, self).__setitem__(*args)


class Emul(object):
    def __init__(self, opcodes, noun=None, verb=None, inbuf=list()):
        if isinstance(opcodes, str):
            opcodes = [int(i) for i in opcodes.split(",")]
        self.program = LiberalList(opcodes.copy(), default=0)
        # Not trying to make a new class that inherits from list right now...
        self.logger = logging.getLogger('Intcode Logger')
        self.inst_indx = 0
        if isinstance(noun, int) and isinstance(verb, int):
            self.program[1:3] = noun, verb
        self.am = self.bm = self.cm = self.de = 0
        self.inbuf = inbuf.copy()
        self.inbuf.reverse()
        self.outbuf = list()
        self.last_output = None
        self.execution_complete = False
        self.waiting = False
        self.relative_base = 0
        self.run()

    def parse_mode(self, op):
        """Parse opcode for parameter mode mask"""
        cm, bm, am, d, e = str(op).rjust(5, '0')
        self.cm, self.bm, self.am = int(cm), int(bm), int(am)
        self.de = int(d + e)

    def mode(self, val, mask):
        """Return the vlaue to be used based on the mode-mask.
        Does not work for lvalue, but apparently that is outside of the scope
        of this excersize and this language. """
        # split up
        ind, val = val
        if mask == 1:
            return val
        elif mask == 2:
            return self.program[self.relative_base + val]
        else:
            return self.program[val]

    def add(self, args):
        op, a, b, c = args
        # print(op, a, b, c)
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        _, c = c

        if self.cm == 2:
            c += self.relative_base
        # c = self.mode(c, self.cm)
        self.program[c] = a + b
        self.logger.info(f'ADD: {a} + {b} = {self.program[c]}')
        self.inst_indx += 4

    def mul(self, args):
        op, a, b, c = args
        # print(op, a, b, c)
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        # c = self.mode(c, self.cm)
        _, c = c

        if self.cm == 2:
            c += self.relative_base
        self.program[c] = a * b
        self.logger.info(f'MUL: {a} * {b} = {self.program[c]}')
        self.inst_indx += 4

    def inp(self, args):
        op, a = args
        # a = self.mode(a, self.am)
        _, a = a
        if self.am == 2:
            a += self.relative_base
        if len(self.inbuf) < 1:
            self.waiting = True
            self.logger.info("INP: waiting for input")
            return
        val = self.inbuf.pop()
        self.program[a] = val
        self.logger.info(f"INP: Addr {a} = {val}")
        self.inst_indx += 2

    def out(self, args):
        op, a = args
        res = self.mode(a, self.am)
        self.last_output = res
        # print(f"OUTPUT: {res}")
        self.logger.info(f'OUTPUT: {res}')
        self.outbuf.append(res)
        self.inst_indx += 2

    def jmp_if(self, args):
        op, a, b = args
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        if (self.de == 5 and a) or (self.de == 6 and not a):
            self.inst_indx = b
            self.logger.info(f'JMP-if True: {self.inst_indx}')
        else:
            self.logger.info(f'JMP-if False')
            self.inst_indx += 3

    def mod_rel(self, args):
        op, a = args
        # a = self.mode(a, self.am)
        a = self.mode(a, self.am)
        self.logger.info(f'REL mod : {self.relative_base} + {a}')
        self.relative_base += a
        self.inst_indx += 2

    def lt(self, args):
        op, a, b, c = args
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        # c = self.mode(c, self.cm)
        _, c = c
        if self.cm == 2:
            c += self.relative_base
        self.program[c] = 1 if a < b else 0
        self.logger.info(f'LT: {a} < {b} ?')
        self.inst_indx += 4

    def eq(self, args):
        op, a, b, c = args
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        # c = self.mode(c, self.cm)
        _, c = c

        if self.cm == 2:
            c += self.relative_base
        self.program[c] = 1 if a == b else 0
        self.logger.info(f'EQ: {a} == {b} ?')
        self.inst_indx += 4

    def run(self):
        self.parse_mode(self.program[self.inst_indx])
        self.waiting = False
        # print(self.inst_indx, self.de)
        while self.execution_complete is not True and self.waiting is False:
            func = None
            self.logger.debug(f'INSTRUCTION INDEX: {self.inst_indx}')
            if self.de == 1:
                nargs = 4
                func = self.add
            elif self.de == 2:
                nargs = 4
                func = self.mul
            elif self.de == 3:
                nargs = 2
                func = self.inp
            elif self.de == 4:
                nargs = 2
                func = self.out
            elif self.de in [5, 6]:
                nargs = 3
                func = self.jmp_if
            elif self.de == 7:
                nargs = 4
                func = self.lt
            elif self.de == 8:
                nargs = 4
                func = self.eq
            elif self.de == 9:
                nargs = 2
                func = self.mod_rel
            elif self.de == 99:
                self.execution_complete = True
                self.logger.info('END')
                break
            else:
                print(f"unrecognized opcode: {self.de}, at position {self.inst_indx}")
                break
            args = enumerate(self.program[self.inst_indx:self.inst_indx + nargs])
            func(args)
            self.parse_mode(self.program[self.inst_indx])
            # print(self.inst_indx, self.de)


class HullPaintingRobot(object):
    def __init__(self, program):
        self._program = program.copy()
        self.brain = Emul(program)
        self.location = (0, 0)
        self.directions = deque(['^', '>', 'v', '<'])
        self.white_locations = list()
        self.painted_locations = set()
        self.location_map = dict()

    def operate(self):
        while self.brain.execution_complete is not True:
            if self.location in self.white_locations:
                self.brain.inbuf.append(1)
            else:
                self.brain.inbuf.append(0)
            self.painted_locations.add(self.location)
            self.brain.run()
            turn_type = self.brain.outbuf.pop()
            new_color = self.brain.outbuf.pop()
            if new_color == 1:
                self.white_locations.append(self.location)
            elif new_color == 0 and self.location in self.white_locations:
                self.white_locations.remove(self.location)

            if turn_type == 0:
                self.directions.rotate(-1)
            else:
                self.directions.rotate(1)

            current_direction = self.directions[0]
            x, y = self.location
            if current_direction == '^':
                y += 1
            elif current_direction == '<':
                x -= 1
            elif current_direction == '>':
                x += 1
            elif current_direction == 'v':
                y -= 1

            self.location = (x, y)

    def print_hull(self):
        self.white_locations.sort(key=lambda a: a[0])
        min_x = self.white_locations[0][0]
        max_x = self.white_locations[-1][0]
        self.white_locations.sort(key=lambda a: a[1])
        min_y = self.white_locations[0][1]
        max_y = self.white_locations[-1][1]
        for y in range(max_y, min_y - 1, -1):
            line = ""
            for x in range(max_x, min_x - 1, -1):
                loc = (x, y)
                line += '#' if loc in self.white_locations else '.'
            print(line)


with open("Day11In.txt", "r") as f:
    content = [int(i) for i in f.read().split(",")]

# logging.basicConfig(level=logging.DEBUG)
robot = HullPaintingRobot(content)
robot.operate()
print(f"Part 1: {len(robot.painted_locations)}")
robot = HullPaintingRobot(content)
robot.white_locations.append((0, 0))
robot.operate()
print("Part 2:")
robot.print_hull()

