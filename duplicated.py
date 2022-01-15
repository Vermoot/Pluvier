#!/usr/bin/python
# coding: utf-8
import sys
import json
from steno import Steno
from steno import Word

dic = {}
picked = []
with open('resources/dicofr.json') as f:
        data = f.readlines()
duplicated = {}
for line in data:
        entry = line.split('\n')
        steno = entry[0].split(':')
        if len(steno) < 2:
                continue
        steno[0] = steno[0].strip()
        steno[1] = steno[1].strip()
        
        if steno[0] in dic :
                duplicated[steno[1]] = steno[0]
                continue
        dic[steno[0]] = steno[1]
        
for dup in duplicated.items():
        print(dup)
