#!/usr/bin/python


class Emul(object):
    def __init__(self, opcodes, noun=None, verb=None):
        self.program = opcodes.copy()
        self.inst_indx = 0
        if isinstance(noun, int) and isinstance(verb, int):
            self.program[1] = noun
            self.program[2] = verb
        self.run()
        self.output = self.program[0]
        self.am = self.bm = self.cm = self.de = 0

    def parse_mode(self, op):
        """Parse opcode for parameter mode mask"""
        cm, bm, am, d, e = str(op).rjust(5, '0')
        self.cm, self.bm, self.am = int(cm), int(bm), int(am)
        self.de = int(d + e)

    def mode(self, val, mask):
        """Return the vlaue to be used based on the mode-mask.
        Does not work for lvalue, but apparently that is outside of the scope
        of this excersize."""
        return val if mask else self.program[val]

    def add(self):
        op, a, b, c = self.program[self.inst_indx:self.inst_indx + 4]
        # print(op, a, b, c)
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        self.program[c] = a + b
        self.inst_indx += 4

    def mul(self):
        op, a, b, c = self.program[self.inst_indx:self.inst_indx + 4]
        # print(op, a, b, c)
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        self.program[c] = a * b
        self.inst_indx += 4

    def inp(self):
        op, a = self.program[self.inst_indx:self.inst_indx + 2]
        self.program[a] = int(input("SIG INPUT>"))
        self.inst_indx += 2

    def out(self):
        op, a = self.program[self.inst_indx:self.inst_indx + 2]
        res = self.mode(a, self.am)
        print(f"OUTPUT: {res}")
        self.inst_indx += 2

    def run(self):
        self.parse_mode(self.program[self.inst_indx])
        # print(self.inst_indx, self.de)
        while self.de != 99:
            if self.de == 1:
                self.add()
            elif self.de == 2:
                self.mul()
            elif self.de == 3:
                self.inp()
            elif self.de == 4:
                self.out()
            else:
                print("unrecognized opcode")
                break
            self.parse_mode(self.program[self.inst_indx])
            # print(self.inst_indx, self.de)


with open("Day5In.txt", "r") as f:
    content = [int(i) for i in f.read().split(",")]

emulator = Emul(content)
print("Part 1: ^^")

