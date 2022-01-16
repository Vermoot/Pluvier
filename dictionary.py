#!/usr/bin/python
# coding: utf-8
import sys
import json
import numpy as np
import json

from steno import Steno
from steno import Word

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
        with open('resources/tao_la_salle.json') as json_file:
            data = json.load(json_file)

        for elem in data.items():
            if elem[0] not in dico:
                dico[elem[0]] = elem[1]
        return dico

    def steno(self,word, force_verb = False):
        self.steno_class=Steno(self.words)
        return self.steno_class.transform_word(word)

    def generate(self) :
        self.words = self.read_corpus()
        self.words.sort(key=lambda x: x.frequence, reverse=True)
#        for word in self.words :
#            print(word.frequence)
#        self.words = self.words[:5000]


        translated_word = {}
        duplicated = []
        translated_word = self.append_tao(translated_word)
        for word in self.words:
            for steno in np.unique(self.steno(word)):
#                steno = steno.replace("'","\'")
                #                    print(steno)
                if steno in translated_word  and (translated_word[steno] == word.word):
                    continue
                if steno in translated_word and '*' not in steno:
                    steno = self.steno_class.add_star(steno)
                    if steno in translated_word :
                        duplicated.append({steno : word.word})
                        duplicated.append({steno : translated_word[steno]  })
                        continue
                    
                translated_word[steno] = word.word

#                    d.write("'"+steno + "':'"+ word.word+"',\n")

        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        dup_object = json.dumps(duplicated, indent = 4, ensure_ascii=False )
        with open('resources/dup.json', "w") as d:
            d.write(dup_object)
        with open('resources/dicofr.json', "w") as d:
            d.write(json_object)

Dictionary().generate()
