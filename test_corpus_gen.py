import sys
import random
import csv

source = sys.argv[1]
dest = sys.argv[2]

lines = ""
with open(source) as f:
    lines = f.readlines()

picked = [0]
for i in range(0,3):
    j = random.randrange(1,len(lines)-20)
    picked.extend(range(j,j+20))

for i in range(0,40):
    picked.append(random.randrange(1,len(lines)))

picked = set(picked)
picked = sorted(picked)
print(picked)
print("len: %i" % len(picked))

with open(dest, "w") as d:
    for line in picked:
        d.write(lines[line])
