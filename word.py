import sys
import copy
import re
class Word:
        def __init__(self, word, phonetics, lemme, cgram, cgramortho,genre, number, info_verb, syll, orthosyll, frequence = 0):
            self.word = word
            self.phonetics = phonetics
            self.lemme = lemme
            self.cgram = cgram
            self.cgramortho = cgramortho
            self.genre = genre
            self.number = number
            self.info_verb = info_verb
            self.syll = syll
            self.orthosyll = orthosyll
            self.frequence = float(frequence)
        def __str__(self):
                print("word", self.word)
                print("phonetics", self.phonetics)
                print("lemme", self.lemme)
                print('cgram',  self.cgram)
                print('number', self.number)
                print('syll', self.syll)
                return self.syll
        
        def is_verb(self):
                return "VER" in self.cgram  or "AUX" in self.cgram #and "AUX" not in self.cgramortho
        
        def is_infinitif(self):
                return 'inf' in self.info_verb

        def is_passe_compose(self):
                if 'ADJ' in self.info_verb:
                        return false
                return 'pas' in self.info_verb and self.word.endswith('é')

        def is_imparfait(self):
                Log(self.info_verb)
                return ':imp' in self.info_verb
        #and self.word.endswith('ait')

        def is_conditionnel(self):
                return 'cnd' in self.info_verb

        def is_third_person_plural(self):
                return '3p' in self.info_verb

        def is_third_person_singular(self):
                return '3s' in self.info_verb

        def is_participe_present(self):
#                return 'par' in self.info_verb and
                return self.is_verb() and self.word.endswith('ant')

        def is_vous_ind_present(self):
                return 'ind' in self.info_verb and self.word.endswith('ez')

        def is_indicatif(self):
                return 'ind' in self.info_verb

        def is_plural(self) :
                return self.number =='p'
