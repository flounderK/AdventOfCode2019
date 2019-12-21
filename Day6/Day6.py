#!/usr/bin/python
from collections import defaultdict, deque


class OrbitRelationalMapper(object):
    def __init__(self, orbit_relationships):
        self.raw_relationships = orbit_relationships
        self.rel_indep_as_key = defaultdict(list)
        self.rel_dep_as_key = dict()
        self.all_objects = set()
        self.start_point = ""
        self.end_points = set()
        self.path_to_obj = dict()
        self.map_relationships()

    def map_relationships(self):
        for indep, dep in self.raw_relationships:
            self.rel_indep_as_key[indep].append(dep)
            self.rel_dep_as_key[dep] = indep
            self.all_objects.add(indep)
            self.all_objects.add(dep)

        # just to ensure that the start point matches with the input
        self.start_point = list(self.all_objects - set(self.rel_dep_as_key.keys()))[0]
        self.end_points = self.all_objects - set(self.rel_indep_as_key.keys())

        seed_obj = self.start_point
        objects_to_use = deque()
        used_objects = set()
        while len(self.all_objects - used_objects) > 0:
            used_objects.add(seed_obj)
            self.map_path_to_obj(seed_obj)

            for branch in self.rel_indep_as_key[seed_obj]:
                objects_to_use.append(branch)
            if len(objects_to_use) > 0:
                seed_obj = objects_to_use.pop()

    def map_path_to_obj(self, name):
        """Starting at the given node, go through each parent node until
        either a known node is found or until the root node is found"""
        path = []
        if name == self.start_point:
            self.path_to_obj[name] = []
            return []
        obj = self.rel_dep_as_key[name]
        while obj != self.start_point:
            path.append(obj)
            if self.path_to_obj.get(obj) is not None:
                path.extend(self.path_to_obj[obj][::-1])
                break
            obj = self.rel_dep_as_key[obj]
        if obj == self.start_point:
            path.append(self.start_point)
        path.reverse()
        self.path_to_obj[name] = path.copy()
        return path

    def find_total_number_of_orbits(self):
        return sum(len(v) for k, v in self.path_to_obj.items())


with open("Day6In.txt", "r") as f:
    content = [tuple(i.split(')')) for i in f.read().split()]
o = OrbitRelationalMapper(content)
p1res = o.find_total_number_of_orbits()
print(f"Part 1: {p1res}")

YOU = o.path_to_obj['YOU']
SAN = o.path_to_obj['SAN']
you_unique = set(YOU).difference(set(SAN))
san_unique = set(SAN).difference(set(YOU))
p2res = len(you_unique) + len(san_unique)
print(f"Part 2: {p2res}")

