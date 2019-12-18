#!/usr/bin/python
import re

puzzle_in = "278384-824795"
start, end = [int(i) for i in puzzle_in.split("-")]

match_list = list()
p2match_list = set()
for i in range(start, end + 1):
    string_num = str(i)[::-1]
    if re.search(r'(\d)\1', string_num) is None:
        continue

    invalid_seq = False
    for s, m in enumerate(string_num):
        if len([k for k in string_num[s:] if int(k) > int(m)]) > 0:
            invalid_seq = True
            break

    if invalid_seq is True:
        continue

    match_list.append(i)

for i in match_list:
    matches = re.findall(r'((\d)\2+)', str(i))
    for largest, match_chr in matches:
        if len(largest) == 2:
            p2match_list.add(i)
print(f"Part 1: {len(match_list)}")
print(f"Part 2: {len(p2match_list)}")

