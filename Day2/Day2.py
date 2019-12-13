

class Emul(object):
    def __init__(self, opcodes):
        self.program = opcodes
        self.inst_indx = 0
        self.run()

    def add(self):
        self.inst_indx += 1
        a = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        b = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        c = self.program[self.program[self.inst_indx]] = a + b
        self.inst_indx += 1
        print(f"{a} + {b} = {c}")

    def mul(self):
        self.inst_indx += 1
        a = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        b = self.program[self.program[self.inst_indx]]
        self.inst_indx += 1
        c = self.program[self.program[self.inst_indx]] = a * b
        self.inst_indx += 1
        print(f"{a} + {b} = {c}")

    def run(self):
        while self.program[self.inst_indx] != 99:
            if self.program[self.inst_indx] == 1:
                self.add()
            elif self.program[self.inst_indx] == 2:
                self.mul()
            else:
                print("unrecognized opcode")
                break
        # print(",".join([str(i) for i in self.program]))


with open("Day2In.txt", "r") as f:
    content = [int(i) for i in f.read().split(",")]

altered_content = content.copy()
altered_content[1] = 12
altered_content[2] = 2
emulator = Emul(altered_content)

p1res = emulator.program[0]
print(f"Part 1: {p1res}")
