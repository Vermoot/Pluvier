#!/usr/bin/python
# coding: utf-8
import sys
import json
import numpy as np
import json

from src.steno import Steno
from src.steno import Word

class Dictionary:

    picked = []
    words = []

    source = "resources/Lexique383.tsv"
    def read_corpus(self):
        words = []
        first_line = True
        with open(self.source) as f:
            corpus = f.readlines()
            
            for line in corpus:
                if first_line:
                    first_line = False
                    continue
                entry = line.split("\t")
                word = Word(word = entry[0],
                            phonetics = entry[1],
                            lemme = entry[2],
                            cgram = entry[3],
                            cgramortho = entry[28],
                            genre = entry[4],
                            number = entry[5],
                            info_verb = entry[10],
                            syll = entry[22],
                            orthosyll = entry[27],
                            frequence = entry[6]
                            )
                words.append(word)
                
        return words

    def generate(self) :
        # with open('resources/dicofr.json') as json_file:
        #     data = json.load(json_file)
        # translated_word = self.append_tao(data)
        # return True
        self.words = self.read_corpus()

        self.words.sort(key=lambda x: x.frequence, reverse=True)
#        for word in self.words :
#            print(word.frequence)
#        self.words = self.words[:6000]

        with open('resources/dicofr.json') as json_file:
            dicofr = json.load(json_file)
        with open('resources/verbs.json') as json_file:
            verbs= json.load(json_file)

        translated_word = {}
        duplicated = {}

        for word in self.words:
            if not word.is_plural():
                continue
            for steno, val in dicofr.items():
                if val != word.lemme:
                    continue
                if steno[-1] == 'S':
                    if (steno+'Z' in dicofr) or (steno+'Z' in verbs) :
                        duplicated[steno+'Z'] = word.word
                        continue

                    translated_word[steno+'Z'] = word.word
                    continue
                if steno[-1] == 'Z':
                    duplicated[steno] = word.word
                    continue
                if steno+'S' in dicofr:
                    duplicated[steno+'S'] = word.word 
                    continue

                if steno+'S' in verbs:
                    duplicated[steno+'S'] = word.word 
                    continue


                translated_word[steno+'S'] = word.word

            

#                    d.write("'"+steno + "':'"+ word.word+"',\n")
        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        dup_object = json.dumps(duplicated, indent = 4, ensure_ascii=False )
        with open('resources/dup-plural.json', "w") as d:
            d.write(dup_object)
        with open('resources/dicofr-plural.json', "w") as d:
            d.write(json_object)

Dictionary().generate()
