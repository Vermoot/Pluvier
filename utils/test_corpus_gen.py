import sys
import random
import csv

source = sys.argv[1]
dest = sys.argv[2]

lines = ""
with open(source) as f:
    lines = f.readlines()

picked = [0]

#  Blocks of 20 words
for i in range(0,5):
    j = random.randrange(1,len(lines)-20)
    picked.extend(range(j,j+20))

#  Singles
for i in range(0,80):
    picked.append(random.randrange(1,len(lines)))

picked = set(picked)
picked = sorted(picked)
print(picked)
print("len: %i" % len(picked))

with open(dest, "w") as d:
    for line in picked:
        d.write(lines[line])
