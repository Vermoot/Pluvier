#!/usr/bin/python
# coding: utf-8
import sys
import json
import numpy as np
import json

from src.steno import Steno
from src.word import Word

class Abbreviation:

    picked = []
    words = []

    source = "resources/Lexique383.tsv"

    def contraction_exists(self,data, word):
        for steno, val in data.items():
            if val != word:
                continue
            if steno.count('/') < 2:
                return True

        return False


    def generate(self) :
        with open('resources/dicofr.json') as json_file:
             data = json.load(json_file)
        with open('resources/verbs.json') as json_file:
            verbs= json.load(json_file)
        translated_word = {}
        dup = {}
        for elem_steno, elem_word in data.items():
            if elem_steno.count('/') < 2:
                continue
            if self.contraction_exists(data, elem_word):
                continue
            words = elem_steno.split('/')
            word = words[0]+'/'+words[1]+'/'+words[-1]

            if elem_steno.count('/') == 3:
                word = words[0]+'/'+words[-1]
            print(word)            
            if (word[-1] not in data) and (word not in data) and (word not in translated_word) and (word[-1] not in verbs) and (word not in verbs):
                translated_word[word] = elem_word
                continue
                
            if (word in translated_word):
                if elem_steno not in dup:
                    dup[elem_steno] =[]
                    dup[elem_steno].append(translated_word[word])
                    dup[elem_steno].append(word)
                    translated_word.pop(word)
            

#                    d.write("'"+steno + "':'"+ word.word+"',\n")

        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        with open('resources/abbrev.json', "w") as d:
            d.write(json_object)
        dup_object = json.dumps(dup, indent = 4, ensure_ascii=False )
        with open('resources/dup-abbrev.json', "w") as d:
            d.write(dup_object)


Abbreviation().generate()
