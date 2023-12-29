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
    def append_tao(self, dico):
        dup = {}
        with open('resources/tao_la_salle_simple.json') as json_file:
            data = json.load(json_file)

        for elem in data.items():
            if elem[0] in dico and dico[elem[0]] != elem[1]:
                if elem[0] not in dup:
                    dup[elem[0]] =[]
                dup[elem[0]].append(dico[elem[0]])
                dup[elem[0]].append(elem)
            dico[elem[0]] = elem[1]
        dup_object = json.dumps(dup, indent = 4, ensure_ascii=False )
        with open('resources/dup-tao.json', "w") as d:
            d.write(dup_object)

        return dico

    def steno(self,word, force_verb = False):
        self.steno_class=Steno(self.words)
        return self.steno_class.newtransform(word)

    def generate(self) :
        # with open('resources/dicofr.json') as json_file:
        #     data = json.load(json_file)
        # translated_word = self.append_tao(data)
        # return True
        self.words = self.read_corpus()

        self.words.sort(key=lambda x: x.frequence, reverse=True)
#        for word in self.words :
#            print(word.frequence)
#        self.words = self.words[:60000]
        with open('resources/alone.json') as json_file:
            tao = json.load(json_file)

        translated_word = {}
        duplicated = {}

        for word in self.words:
#            if word.word  in tao.values():
#                continue
 
            if word.is_verb() and not word.is_infinitif():
                continue
            for steno in np.unique(self.steno(word)):
                if steno in tao.keys():
                    continue
#                steno = steno.replace("'","\'")
                #                    print(steno)
                if steno in translated_word  and (translated_word[steno] == word.word):
                    continue
                if steno in translated_word:

                    if word.word  in tao.values():
                        continue
 
                    original = steno
                    if  '*' not in steno:
                        steno = self.steno_class.add_star_on_word(steno)
                    if steno in translated_word :
                        if steno not in duplicated:
                            duplicated[steno] = []
                            duplicated[steno].append(translated_word[original])
                        if word.word not in duplicated[steno]:
                            duplicated[steno].append(word.word)
                        if translated_word[steno]  not in duplicated[steno]:
                            duplicated[steno].append(translated_word[steno])
                        continue
                    
                translated_word[steno] = word.word

#                    d.write("'"+steno + "':'"+ word.word+"',\n")
#        translated_word = self.append_tao(translated_word)
        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        dup_object = json.dumps(duplicated, indent = 4, ensure_ascii=False )
        with open('resources/dup.json', "w") as d:
            d.write(dup_object)
        with open('resources/dicofr.json', "w") as d:
            d.write(json_object)

Dictionary().generate()

# replace all /TPH' by /-B'
