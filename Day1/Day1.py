import math


def get_required_fuel(mass):
    return math.floor(mass / 3) - 2


with open("Day1In.txt", "r") as f:
    content = [int(i) for i in f.read().split()]

p1result = sum([get_required_fuel(i) for i in content])
r = lambda a: r(y) + a if (y := get_required_fuel(a)) > 0 else a
p2result = sum([r(get_required_fuel(i)) for i in content])

print(f"Part 1: {p1result}")
print(f"Part 2: {p2result}")

