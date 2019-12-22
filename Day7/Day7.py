#!/usr/bin/python
from itertools import permutations


class Emul(object):
    def __init__(self, opcodes, noun=None, verb=None, inbuf=None):
        if isinstance(opcodes, str):
            opcodes = [int(i) for i in opcodes.split(",")]
        self.program = opcodes.copy()
        self.inst_indx = 0
        if isinstance(noun, int) and isinstance(verb, int):
            self.program[1] = noun
            self.program[2] = verb
        self.am = self.bm = self.cm = self.de = 0
        self.inbuf = inbuf.copy()
        self.inbuf.reverse()
        self.last_output = None
        self.execution_complete = False
        self.waiting = False
        self.run()

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
        if len(self.inbuf) < 1:
            self.waiting = True
            print("waiting for input")
            return
        val = self.inbuf.pop()
        self.program[a] = val
        self.inst_indx += 2

    def out(self):
        op, a = self.program[self.inst_indx:self.inst_indx + 2]
        res = self.mode(a, self.am)
        self.last_output = res
        print(f"OUTPUT: {res}")
        self.inst_indx += 2

    def jmp_if(self):
        op, a, b = self.program[self.inst_indx:self.inst_indx + 3]
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        if (self.de == 5 and a) or (self.de == 6 and not a):
            self.inst_indx = b
        else:
            self.inst_indx += 3

    def lt(self):
        op, a, b, c = self.program[self.inst_indx:self.inst_indx + 4]
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        self.program[c] = 1 if a < b else 0
        self.inst_indx += 4

    def eq(self):
        op, a, b, c = self.program[self.inst_indx:self.inst_indx + 4]
        a = self.mode(a, self.am)
        b = self.mode(b, self.bm)
        self.program[c] = 1 if a == b else 0
        self.inst_indx += 4

    def run(self):
        self.parse_mode(self.program[self.inst_indx])
        self.waiting = False
        # print(self.inst_indx, self.de)
        while self.execution_complete is not True and self.waiting is False:
            if self.de == 1:
                self.add()
            elif self.de == 2:
                self.mul()
            elif self.de == 3:
                self.inp()
            elif self.de == 4:
                self.out()
            elif self.de in [5, 6]:
                self.jmp_if()
            elif self.de == 7:
                self.lt()
            elif self.de == 8:
                self.eq()
            elif self.de == 99:
                self.execution_complete = True
            else:
                print("unrecognized opcode")
                break
            self.parse_mode(self.program[self.inst_indx])
            # print(self.inst_indx, self.de)


with open("Day7In.txt", "r") as f:
    content = [int(i) for i in f.read().split(",")]

results = list()
for perm in permutations([0, 1, 2, 3, 4], 5):
    out = 0
    for s in perm:
        out = Emul(content, inbuf=[s, out]).last_output
    results.append(("".join(str(i) for i in perm), out))

results.sort(key=lambda a: a[1], reverse=True)
p1res = results[0][1]
print(f"Part 1: {p1res}")

results = list()
for perm in permutations([5, 6, 7, 8, 9], 5):
    print("starting next setting permutation")
    out = 0
    amps = list()
    for s in perm:
        amp = Emul(content, inbuf=[s, out])
        amps.append((s, amp))
        out = amp.last_output
    while len([amp for s, amp in amps if amp.execution_complete is True]) < len(amps):
        for s, amp in amps:
            amp.inbuf = [out]
            amp.run()
            out = amp.last_output
    results.append(("".join(str(i) for i in perm), out))


results.sort(key=lambda a: a[1], reverse=True)
p2res = results[0][1]
print(f"Part 2: {p2res}")
