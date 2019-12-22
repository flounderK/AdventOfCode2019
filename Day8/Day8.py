#!/usr/bin/python


def batch(it, size):
    l = len(it)
    for i in range(0, l, size):
        yield it[i:i + size]


with open("Day8In.txt", "r") as f:
    content = f.read().strip()

layers = [i for i in batch(content, 25*6)]

p1layer = sorted(layers, key=lambda x: x.count('0'))[0]
p1res = p1layer.count('1') * p1layer.count('2')
print(f"Part 1: {p1res}")

print("Part 2: ")
for r in range(0, 6):
    col = ""
    for c in range(0, 25):
        for i, layer in enumerate(layers):
            px = layer[(r * 25) + c]
            if px == '0':
                col += ' '
            elif px == '1':
                col += '#'
            elif px == '2':
                continue
            break
    print(col)


