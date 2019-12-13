

class Emul(object):
    def __init__(self, opcodes, noun=None, verb=None):
        self.program = opcodes.copy()
        self.inst_indx = 0
        if isinstance(noun, int) and isinstance(verb, int):
            self.program[1] = noun
            self.program[2] = verb
        self.run()
        self.output = self.program[0]

    def add(self):
        self.inst_indx += 1
        a = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        b = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        c = self.program[self.program[self.inst_indx]] = a + b
        self.inst_indx += 1
        # print(f"{a} + {b} = {c}")

    def mul(self):
        self.inst_indx += 1
        a = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        b = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        c = self.program[self.program[self.inst_indx]] = a * b
        self.inst_indx += 1
        # print(f"{a} * {b} = {c}")

    def run(self):
        while self.program[self.inst_indx] != 99:
            if self.program[self.inst_indx] == 1:
                self.add()
            elif self.program[self.inst_indx] == 2:
                self.mul()
            else:
                # print("unrecognized opcode")
                break
        # print(",".join([str(i) for i in self.program]))


with open("Day2In.txt", "r") as f:
    content = [int(i) for i in f.read().split(",")]

emulator = Emul(content, 1, 2)

p1res = emulator.output
print(f"Part 1: {p1res}")

for a, b in [(a, b) for a in range(99) for b in range(99)]:
    emulator = Emul(content, a, b)
    if emulator.output == 19690720:
        break
p2res = (100 * a) + b
print(f"Part 2: {p2res}")
