#!/usr/bin/python
# coding: utf-8
import sys
import re
import numpy as np
import json

from src.steno import Steno
from src.word import Word

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
    def add_pronoun_je(self, steno,word):
        if word.is_first_person_singular():
                    pronoun='je '
                    if re.match("^[aeiouyh]",word.word):
                        pronoun="j'"
                    if steno[0] in ['E','A','U','O','-']: 
                        translated_word["SKWR"+steno] = pronoun+word.word
                    else:
                        translated_word["SKWR/"+steno] = "je "+word.word
        
    def append_tao(self, dico):
        dup = {}
        with open('resources/tao_la_salle.json') as json_file:
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
        with open('resources/tao_la_salle.json') as json_file:
            tao = json.load(json_file)


#        for word in self.words :
#            print(word.frequence)
#         self.words = self.words[:80000]


        translated_word = {}
        duplicated = {}

        for word in self.words:
            if not word.is_verb():
                continue
                        
            # if word.is_first_person_singular():
            #     word.syll ='Z°' + word.syll
            #     word.phonetics ='Z°' + word.phonetics
            #     word.word ='je ' + word.word

            stenowords = self.steno(word)
            if len(stenowords)==0:
                continue

            for steno in np.unique(stenowords):
#                steno = steno.replace("'","\'")
                #                    print(steno)
                if steno in translated_word  and (translated_word[steno] == word.word):
                    continue

                if steno in translated_word:
                    if  '*' not in steno:
                        steno = self.steno_class.add_star_on_word(steno)
                    if steno in translated_word :
                        if steno not in duplicated:
                            duplicated[steno] = []
                        if word.word not in duplicated[steno]:
                            duplicated[steno].append(word.word)
                        if translated_word[steno]  not in duplicated[steno]:
                            duplicated[steno].append(translated_word[steno])
                        continue
                translated_word[steno] = word.word
                if word.frequence<10:
                    continue
                if word.is_first_person_singular():
                    
                    pronoun='je '
                    if re.match("^[aeiouyh]",word.word):
                        pronoun="j'"
                    if steno[0] in ['E','A','U','O','-']: 
                        translated_word["SKWR"+steno] = pronoun+word.word
                    else:
                        translated_word["SKWR/"+steno] = pronoun+word.word
                if word.is_second_person_singular():
                    pronoun='tu '

                    if steno[0] in ['R','E','A','U','O','-']: 
                        translated_word["TW"+steno] = pronoun+word.word
                    else:
                        translated_word["TW/"+steno] = pronoun+word.word
                if word.is_third_person_singular():
                    pronoun='il '

                    if steno[0] in ['E','A','U','O','-']: 
                        translated_word["KWR"+steno] = pronoun+word.word
                    else:
                        translated_word["KWR/"+steno] = pronoun+word.word
                    pronoun='elle '

                    if steno[0] in ['E','A','U','O','-']: 
                        translated_word["HR"+steno] = pronoun+word.word
                    else:
                        translated_word["HR/"+steno] = pronoun+word.word
                        


#                    d.write("'"+steno + "':'"+ word.word+"',\n")

        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        dup_object = json.dumps(duplicated, indent = 4, ensure_ascii=False )
        with open('resources/dup-verbs.json', "w") as d:
            d.write(dup_object)
        with open('resources/verbs.json', "w") as d:
            d.write(json_object)

Dictionary().generate()
