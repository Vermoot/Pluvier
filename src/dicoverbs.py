import sys
import re
import numpy as np
import json

from copy import copy, deepcopy

from src.steno import Steno
from src.dictionary import Dictionary
from src.word import Word

class Dico_Verbs:
    first_letters_je=['E','A','U','O','-','*'];
    first_letters_tu=['E','A','U','O','-','*','R','H'];

    picked = []
    words = []

    def test_je(self,steno):
        if  steno.endswith('RAEUS'):
            return steno[:-5]+'R-S'
                        
        if  steno.endswith('/AEUS')  :
            return steno[:-5]+'/-S'
        if steno.endswith('/A*EUS')  :
            return steno[:-6]+'/-S'
        if  steno.endswith('/AEU'):
            return steno[:-4]+'/-S'
        if  steno.endswith('T/-S'):
            return steno[:-4]+'TS'
        return steno


    def add_pronoun_je(self, steno,word):
        if word.is_first_person_singular():
                    pronoun='je '
                    print('iici'+steno)
                    if word.is_imparfait() and steno.endswith('/AEUS'):

                        steno=steno[5:]+'/-S'

                    if re.match("^[aeéiouyh]",word.word):
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

    def generate_steno(self, word,stenowords, translated_word) :
        for steno in np.unique(stenowords):
#                steno = steno.replace("'","\'")
                #                    print(steno)
                if steno in translated_word  and (translated_word[steno] == word.word):
                    continue

                # if steno in translated_word:
                #     if  '*' not in steno:
                #         steno = self.steno_class.add_star_on_word(steno)
                #     if steno in translated_word :
                #         if steno not in duplicated:
                #             duplicated[steno] = []
                #         if word.word not in duplicated[steno]:
                #             duplicated[steno].append(word.word)
                 #         if translated_word[steno]  not in duplicated[steno]:
                #             duplicated[steno].append(translated_word[steno])
                #         continue
#                translated_word[steno] = word.word

                if word.is_first_person_singular():
                    newsteno=deepcopy(steno)
                    pronoun='je '
                    newsteno  = self.test_je(newsteno)
                    if re.match("^[aeéiouyh]",word.word):
                        pronoun="j'"
                    if steno[0] in self.first_letters_je: 
                        translated_word["SKWR"+newsteno] = pronoun+word.word
                    else:
                        translated_word["SKWR/"+newsteno] = pronoun+word.word

#                    if newsteno[0] in ['E','A','U','O','-']: 
#                    translated_word[newsteno] = pronoun+word.word
 #                   else:
  #                      translated_word["SKWR/"+newsteno] = pronoun+word.word
                if word.is_second_person_singular():
                    pronoun='tu '
                    newsteno=deepcopy(steno)
                    newsteno  = self.test_je(newsteno)
                    if steno[0] in self.first_letters_tu: 
                        translated_word["TW"+newsteno] = pronoun+word.word
                    else:
                        translated_word["TW/"+newsteno] = pronoun+word.word
                if word.is_third_person_singular():
                    newsteno=deepcopy(steno)
                    pronoun='il '

                    if steno[0] in self.first_letters_je: 
                        translated_word["KWR"+steno] = pronoun+word.word
                    else:
                        translated_word["KWR/"+steno] = pronoun+word.word
                    pronoun='elle '

                    if steno[0] in self.first_letters_je: 
                        translated_word["HR"+steno] = pronoun+word.word
                    else:
                        translated_word["HR/"+steno] = pronoun+word.word
                        

        return translated_word
#                    d.write("'"+steno + "':'"+ word.word+"',\n")

    def generate(self) :
        # with open('resources/dicofr.json') as json_file:
        #     data = json.load(json_file)
        # translated_word = self.append_tao(data)
        # return True
        self.words = Dictionary().read_corpus()
        self.words.sort(key=lambda x: x.frequence, reverse=True)
        with open('resources/tao_la_salle.json') as json_file:
            tao = json.load(json_file)


        for word in self.words :
            print(word.frequence)
        self.words = self.words[:80000]


        translated_word = {}
        duplicated = {}

        for word in self.words:
            if not word.is_verb():
                continue
                        
            # if word.is_first_person_singular():
            #     word.syll ='Z°' + word.syll
            #     word.phonetics ='Z°' + word.phoneticsbien
            #     word.word ='je ' + word.word

            if word.is_first_person_singular():
                newword=deepcopy(word)
#                newword.syll ='Z' + word.syll
#                newword.phonetics ='Z' + word.phonetics
 #               word.word ='je ' + word.word
                stenowords = self.steno(newword)
                
                if len(stenowords)==0:
                    continue
                translated_word=self.generate_steno(newword,stenowords,translated_word)
            if word.is_second_person_singular():
                newword=deepcopy(word)
                newword.syll ='tw' + word.syll
                stenowords = self.steno(newword)
                translated_word=self.generate_steno(newword,stenowords,translated_word)
            
            if word.is_third_person_singular():
                newword=deepcopy(word)
                newword.syll ='l' + word.syll
                stenowords = self.steno(newword)
                translated_word=self.generate_steno(newword,stenowords,translated_word)
            

        json_object = json.dumps(translated_word, indent = 4, ensure_ascii=False )
        dup_object = json.dumps(duplicated, indent = 4, ensure_ascii=False )
        with open('resources/dup-verbs.json', "w") as d:
            d.write(dup_object)
        with open('resources/verbs.json', "w") as d:
            d.write(json_object)
