#!/usr/bin/python
import re


class Moon(object):
    MOONS = list()
    TOTAL_STEPS = 0
    PAST_STATES = dict()

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xv = self.yv = self.zv = 0
        self._xm = self._ym = self._zm = 0
        self.__class__.MOONS.append(self)
        self._save_state()

    @classmethod
    def time_step(cls):
        cls.TOTAL_STEPS += 1
        tmp = [(a, b) for a in cls.MOONS for b in cls.MOONS if a != b]
        pairs = list()
        for a, b in tmp:
            if (b, a) not in pairs:
                pairs.append((a, b))

        for m1, m2 in pairs:
            for prop, modprop in [("x", "xv"), ("y", "yv"), ("z", "zv")]:
                cls.__find_velocity_mod(m1, m2, prop, modprop)

        for moon in cls.MOONS:
            moon.x += moon.xv
            moon.y += moon.yv
            moon.z += moon.zv

        cls._save_state()

    @staticmethod
    def __find_velocity_mod(moon1, moon2, prop, modprop):
        if getattr(moon1, prop) != getattr(moon2, prop):
            m2_val, m1_val = (1, -1) if getattr(moon1, prop) > getattr(moon2, prop) else (-1, 1)
            setattr(moon2, modprop, getattr(moon2, modprop) + m2_val)
            setattr(moon1, modprop, getattr(moon1, modprop) + m1_val)

    def get_total_energy(self):
        potential = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic = abs(self.xv) + abs(self.yv) + abs(self.zv)
        return potential * kinetic

    def __repr__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, " + \
               f"vel=<x={self.xv}, y={self.yv}, z={self.zv}>"

    def get_state(self):
        pos = (self.x, self.y, self.z)
        vel = (self.xv, self.yv, self.zv)
        return (pos, vel)

    @classmethod
    def get_class_state(cls):
        return tuple(map(lambda m: m.get_state(), cls.MOONS))

    @classmethod
    def _save_state(cls):
        # use a tuple so that it is not mutable and can be a key in a dict
        state = cls.get_class_state()
        if cls.PAST_STATES.get(state) is None:
            cls.PAST_STATES[state] = 1
        else:
            cls.PAST_STATES[state] += 1


with open("Day12In.txt", "r") as f:
    content = f.read()

content1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
content2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

content = [re.search(r'x=(-*\d+), y=(-*\d+), z=(-*\d+)', i)
           for i in content.split('\n') if i != '']

content = [tuple(map(lambda a: int(a), i.groups())) for i in content
           if i is not None]

for args in content:
    Moon(*args)

print("step 0")
for m in Moon.MOONS:
    print(m)
print("")

for i in range(1, 1001):
    print(f"Step {i}")
    Moon.time_step()
    for m in Moon.MOONS:
        print(m)
    print("")

p1res = sum([moon.get_total_energy() for moon in Moon.MOONS])
print(f"Part 1: {p1res}")
# This is technically a solution for part 2, but it is very inefficient.
# I will come back to this, but a better solution would be to find the rate of
# state repetition for each individual moon, then find the
# lowest common multiple for all of the moons
# state_found_twice = False
# while state_found_twice is False:
#     Moon.time_step()
#     if Moon.PAST_STATES[Moon.get_class_state()] > 1:
#         state_found_twice = True
#         break
#
# print(f"Part 2: {Moon.TOTAL_STEPS}")

