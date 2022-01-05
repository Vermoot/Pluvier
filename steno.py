import sys
import re
class Word:
        def __init__(self, word, phonetics, lemme, cgram, cgramortho,genre, number, info_verb, syll, orthosyll):
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
        def __str__(self):
                print("word", self.word)
                print("phonetics", self.phonetics)
                print("lemme", self.lemme)
                print('cgram',  self.cgram)
                print('number', self.number)
                print('syll', self.syll)
                return self.syll
        
        def is_verb(self):
                return "VER" in self.cgram  and "AUX" not in self.cgramortho
        
        def is_infinitif(self):
                return 'inf' in self.info_verb

        def is_passe_compose(self):
                return 'pas' in self.info_verb and self.word.endswith('é')

        def is_imparfait(self):
                return 'imp' in self.info_verb and self.word.endswith('ait')

        def is_conditionnel(self):
                return 'cnd' in self.info_verb and self.word.endswith('rait')

        def is_participe_present(self):
                return 'par' in self.info_verb and self.word.endswith('ant')

        def is_vous_ind_present(self):
                return 'ind' in self.info_verb and self.word.endswith('ez')


class Ortho:

        sounds = ''
        replace_by = ''
        steno_str =''
        prefix = False
        def __init__(self,sound, replace_by):
                self.sounds = sound.split('|')
                self.replace_by = replace_by

        def steno(self):
                return self.steno_str
        
        def matches(self,word, pattern) :
                return  word.word.endswith(pattern)



class OrthoSuffix(Ortho):
        def convert(self,word) :
                for sound in self.sounds:
                        if word.syll.endswith(sound) :
                                word.syll = word.syll[:-len(sound)]
                                self.steno_str = self.replace_by
#                                print('ortho suffix convert',word.syll)
                                return word
                return word

class OrthoPrefix(Ortho):
        def convert(self,word):
                for sound in self.sounds:
                        if word.syll.startswith(sound) :
                                word.syll = word.syll[len(sound):]
                                self.steno_str = self.replace_by
#                                print('ortho prefix convert',word.syll)
                                return word
                return word
class Steno:
        PREFIXES = {
#                "s2": "S", # ce mais pas ceux

                "tEkno" : "T",
                "tEl" : "THR-",
                'ade' : 'AD-', # sound
                'm°n' : "KH",#men
                'min' : "KH",#min
                'm2n' : 'KH', #men
                "@t" :"SPW",
                "5t" :"SPW",
                "R°" : "R-",
                "S°" : "SK",
                "Sa" : "SK",
                'ke' : 'K',
                'dR' : 'DR',
                'sin' : 'STPH',
                'sn' : 'STPH',
                'k§' : 'KON', # conte
#                'k§' : 'KOEN', # con
                'du' : 'DOU',
                'S' : 'SH',
                "e" : "",
                'ad' : 'AD-', # sound 
                "Z" : "J",
#                'd' : 'DAOE',
                'z' : 'Z',
                
        }

        ORTHO_PREFIXES = {
                "comm" : OrthoPrefix('ko-m|kOm','KM'),
                "com" : OrthoPrefix('k§','K*-'),
                'ind' : OrthoPrefix('5-d', 'SPW'),
                'end' : OrthoPrefix('@-d', 'SPW'),
                
#                "a" : OrthoPrefix('a-','AE-'), # sound

                }

        
        ORTHO_SUFFIXES = {
                'cation' : OrthoSuffix('ka-sj§','-BGS'),
                'ance' : OrthoSuffix('@s', '-NS'),
                'ence' : OrthoSuffix('@s', '-NS'),
                'ande' : OrthoSuffix('@d', '-ND'),
                "elle" : OrthoSuffix("El", "-/*EL"),
                "teur" : OrthoSuffix("t9R", "-/RT") ,
                "trice" : OrthoSuffix("tRis", "-/RTS") ,
                'cienne' : OrthoSuffix('sjEn', '-GZ'),
                'cien' : OrthoSuffix('sj5', '-GS'),
                "ain" : OrthoSuffix("5", "IN"),
                'cte' : OrthoSuffix('kt', 'KT'),
                "ène" : OrthoSuffix("En","-/*EB"),
                "uel" : OrthoSuffix("8El","-/W*EL"),
                "che" : OrthoSuffix("S","-/FP"),
                "ué" : OrthoSuffix("8e","-/W*E"),
                "el" : OrthoSuffix("El", "-/*EL"),

                "a" : OrthoSuffix("a", "-/*Z"),
                

        }
                

        REAL_SUFFIXES = {
                "En" : "A*IB",
                "wE": "-/W*E",


        }

        # if start with - then dont convert 
        SUFFIXES = {
                "zj§": "-GZ",
                'sjOn' :'-GZ',

#second option                'sjOn' :'-/GS/*B',
                
                "jEm" : "-/A*EPL",
                "jER" : "AER" , #caissiERE
                "jasm" : "-/KWRAFPL",
                "jEn": "AEB",
                "sj§" : "GS",

                "pid" : "-PD",
                "fis" : "-WEUS",
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                "kEl" : "-BLG",
                'kE' : 'KE',
#                "je" : "AER" , #caissIER
                "loZik" : "LOIK",
                "lOZist" : "-/HRO*EUS",
                "lOg" : "LO*EG",
                "p9R" : "-RP",
#                "l9R" : "-RL",
                "d9R" : "RD",
                "dabl" : "-/TKABL",
                
                "jast" : "YA*S",
                "vwaR" : "-FRS",
                "ks": "-BGS",
                "Ral" : "-RL",
                "Ribl" : "-RBL",
                "@tR" : "-NTS", #-ntre
                "stR" : "-TS", #-ntre
                "RtR" : "-RTS", #-rtre
                "§bl": "-OFRBL",  # comble
                "@bR": "-AFRBS",   # ambre
                "5bR": "-EUFRBS",  # timbre
                "§bR": "-OFRBS",   # ombre
                "@sj§": "APBGS",    # p_ension_
                "tEkt" : "-/T*K",
                "EtR" : "--TS",
                "SEt" : "-/FPT" , # achete
#                "RZ" : "-/RPBLG",
                "RZ" : "RG",
                "bl" : "-BL",
                "@-S°" : "-AFRPBLG",
                "fR" : "-/FR", #souffre
                "fl" : "-/FL", #souffle
                "RS" : "-FRPB",
                "Re":"-/R*E",
                'z§':'-GZ',
                "@S" : "-AFRPBLG",
                "st" : "-*S",
                "ZE" : "G",
                "S" : "-/FRPBLG",
                "m@" : "-PLT",
                "En" : "AIB",
                "ER" : "AIR",
                "sm" : "-FPL",
                "@d" :"APBD",
                "5b": "-EUFRB",  # limbe
                "§b": "-OFRB",   # tombe
                "@bl": "-AFRBL", # tremble
                "1bl": "-EUFRBL",  # humble
                "dR" : "DZ" ,# ajoin-dre
                "@b": "-AFRB",   # jambe
                "tR": "-TS", #tre
                "bR":"-BS",  #-bre
                "pR":"-PS", #-pre
                "E" : "AEU",
                "n" : "B",
                "nEs" : "BS",
                "§" : "-*PB",
                "sm" : "-/FP",
                
                
        }

        SYLLABE_PLACES = {
                "u-z" : "uz-",
                "R-Si" : "-RSi",
                "@-sj§" : "-@sj§",
                "d-ZEk": "-dZ",
                "b-ZEk": "-bZ",
                "d-Z": "-dZ",
                "S°-" : "S°",
                "vo-l": "vl-",
                "-y-" : "-y",
                "@-t" :"@t-",
                "5-t" :"5t-",
#                'i-j' : 'i',
                'de' : 'd'
        }


        words = []
        suffix = ""
        prefix = ""
        steno_word = ""
        syllabes = []
        ending = ""
        homophones = False
        pronoun = ""
        def __init__(self, corpus):
                self.words = corpus

        def ortho_ending(self, word, init_word) :
                return (word != init_word) and not word.endswith('nt') and not word.endswith('s') and not word.endswith('he') #and not word.endswith('lle')
        
        def find_all_same_syll(self, myword) :
                same_words = []
                if self.homophones:
                        return self.homophones
                for word in self.words:
                        if ((word.syll == myword.syll) and self.ortho_ending(word.word, myword.word)):
                                same_words.append(word)
                
                for word in same_words:
                        print(word.word)
                self.homophones = same_words
                return same_words

        def find_same_word_verb(self, myword) :
                same_words = []
                for word in self.words:
                        if word.word == myword.word and word.is_verb():
                                return word
                return myword

        def find_same_word_not_verb(self, myword) :
                same_words = []
                for word in self.words:
                        if word.word == myword.word and not word.is_verb():
                                return word
                return myword


        def remove_last_syll(self, syll):
                sylls = syll.split('-')
                sylls.pop()
                return "-".join(sylls)

        def orth_ending_iere(self,word, pattern):
                if word.endswith('ière'):
                        return pattern.replace('AER', 'A*ER')
                if word.endswith('ier') and not pattern.endswith('R'):
                        return pattern+'R'
                return pattern

        def orth_write_ending_d(self,word):
                if word.word.endswith('d') and self.has_homophone(word):
                        self.ending = 'D'
                return word

        def ortho_starting_with_des(self,word):
                syll = word.syll.replace('-','')
                print('sp', syll)
#                if not syll.startswith('dez') and not syll.startswith('des') and not syll.startswith('d°s'):
                if not word.word.startswith('de') and not word.word.startswith('dé'):
                        return word
                next_letter = syll[:4].upper()
                print('next letter', next_letter)
                if (next_letter.endswith('O') or next_letter.endswith('E') or next_letter.endswith('I') or next_letter.endswith('A') or next_letter.endswith('U') or next_letter.endswith('@') or next_letter.endswith('Y')) :
                        self.prefix = 'STK'
                        word.syll = word.syll.replace('de-z', '')
                        word.syll = word.syll.replace('de-s', '')
                        word.syll = word.syll.replace('d°-s', '')
                        print('syll repl', word.syll)
                
                return word
                
        def ortho_add_aloneR_infinitif_firstgroup(self, word):
                verb_word = self.find_same_word_verb(word)
                if verb_word.is_verb() and verb_word.is_infinitif()  and verb_word.word.endswith('er'):
                        self.ending = "/-R"
                        if verb_word.syll.endswith('e') :
                                verb_word.syll = verb_word.syll[:-1]
                        return verb_word
                return word

        def ortho_add_alone_keys_on_noun(self,word):
                if word.is_verb():
                        return word
                if word.word.endswith('ette'):
                        self.ending = "/*T"
                        if word.syll.endswith('Et') :
                                print('fini par et')
                                word.syll = word.syll[:-2]
                        return word
                return word

        def ortho_suffixes(self,word):
                for orth in self.ORTHO_SUFFIXES.items():
                        if word.word.endswith(orth[0]):
                                print(vars(orth[1]))
                                ortho = orth[1]
                                word = ortho.convert(word)
                                self.suffix = ortho.steno()
                return word

        def ortho_prefixes(self,word):
                for orth in self.ORTHO_PREFIXES.items():
                        if word.word.startswith(orth[0]):
                                print(vars(orth[1]))
                                ortho = orth[1]
                                ortho.prefix = True
                                word = ortho.convert(word)
                                self.prefix = ortho.steno()
                                return word
                return word

        
        def ortho_add_alone_keys_on_verb(self,word):
                verb_word = self.find_same_word_verb(word)
                if not word.is_verb():
                        return word
                if  verb_word.is_passe_compose():
                        self.ending = "/-D"
                        if verb_word.syll.endswith('e') :
                                verb_word.syll = verb_word.syll[:-1]
                        return verb_word

                if verb_word.is_imparfait():
                        self.ending = "/-S"
                        if verb_word.syll.endswith('E') :
                                verb_word.syll = verb_word.syll[:-1]
                        return verb_word

                if verb_word.is_conditionnel():
                        self.ending = "/-RS"
                        if verb_word.word.endswith('rrait') and verb_word.syll.endswith('E') :
                                verb_word.syll = verb_word.syll[:-1]
                                return verb_word
                        if verb_word.syll.endswith('RE') :
                                verb_word.syll = verb_word.syll[:-2]
                        return verb_word

                if verb_word.is_vous_ind_present():
                        self.ending = "/*EZ"

                        if verb_word.syll.endswith('Re') :
                                self.ending = "/R*EZ"
                                verb_word.syll = verb_word.syll[:-2]
                                return verb_word
                        if verb_word.syll.endswith('e') :
                                verb_word.syll = verb_word.syll[:-1]
                                return verb_word
                if verb_word.is_participe_present():
                        self.ending = "/-G"
#                        if verb_word.syll.endswith('j@')  :
#                                verb_word.syll = verb_word.syll[:-2]
#                                return verb_word
                        if verb_word.syll.endswith('@') :
                                verb_word.syll = verb_word.syll[:-1]
                                return verb_word
                        return verb_word
                
                return word
                
        def try_to_remove_woyel(self, myword) :
                sylls = myword.syll
                same_words=[]
                print('remove last syll',self.remove_last_syll(sylls))
                print('number of i ',len(myword.word.split('i')))
                if ('8i' in self.remove_last_syll(sylls)) or ('i' not in self.remove_last_syll(sylls)) or (len(myword.syll.split('i'))<3):
                        return myword.syll

                sylls = sylls.replace('i','',1)
                        
                for word in self.words:
                        if (self.ortho_ending(word.word, myword.word) and (word.syll.replace('i','',1)==sylls or word.syll.replace('e','',1)==sylls)):
                        #or word.syll.replace('E','',1)==sylls)):
                                same_words.append(word)

                for word in same_words:
                        print('found word same vowel:',word.word)
                if same_words:
                        return myword.syll
                return sylls
        
        def has_homophone(self, word) :
                return self.find_all_same_syll(word)
        
        def find(self,find_word):
                finds = []
                self.pronoun = ''
                if ' ' in find_word:
                        self.pronoun = find_word.split(' ')[0]
                        find_word = find_word.split(' ')[1]
                        
                for word in self.words:
                        if (word.word == find_word):
                                finds.append(word)
                for find_word in finds:
                        if find_word.cgram != "VER":
                                return find_word

                if finds:
                        return finds[0]
                return False

        def change_syllabes(self, word):
                new_word=word
                for syll in self.SYLLABE_PLACES.items():
                        new_word = new_word.replace(syll[0], syll[1])
                return new_word


        def prefixes(self, word, word_class):
                if (word_class.word.startswith('y') and word.startswith('j')):
                        self.prefix ='KWR'
                        new_word = word.replace('j','',1)
                        return new_word
                
                new_word=word
                if  self.pronoun:
                        self.prefix='Y'
                        return word
                for prefix in  self.PREFIXES.items():
                        if len(re.split("^"+prefix[0], new_word))>1:
                                self.prefix = prefix[1]
                                return re.split("^"+prefix[0], new_word)[1]

                return new_word


        def suffixes(self, word):
                new_word=word
                for suffix in  self.SUFFIXES.items():
                        if len(re.split(suffix[0]+"$", new_word))>1:
                                self.suffix = suffix[1]
                                return re.split(suffix[0]+"$", new_word)[0]
                
                return new_word

        def real_suffixes(self, word):
                new_word=word
                for suffix in  self.REAL_SUFFIXES.items():
                        if len(re.split(suffix[0]+"$", new_word))>1:
                                self.suffix = suffix[1]
                                return re.split(suffix[0]+"$", new_word)[0]
                
                return new_word

        def add_star(self,word):
                if (self.ending):
                        return word
                
                return word+"*"
        
        def transform(self,word):
                myword = self.find(word)
                if not myword:
                        return ""
                print(vars(myword))
                myword.syll = self.try_to_remove_woyel(myword)
                print('after remove vowyel', myword.syll)
                self.orth_write_ending_d(myword)
                if self.has_homophone(myword) and myword.is_verb():
                        return self.add_star(self.transform_word(myword))
                myword = self.transform_word(myword)
                myword = self.orth_ending_iere(word, myword)

                return myword
         
        def transform_word(self,word):
                word = self.ortho_suffixes(word)
                word = self.ortho_prefixes(word)
                print('syllabe',word.syll)
                word = self.ortho_add_aloneR_infinitif_firstgroup(word)
                word = self.ortho_add_alone_keys_on_verb(word)
                word = self.ortho_add_alone_keys_on_noun(word)
                if not self.prefix:
                        word = self.ortho_starting_with_des(word)
                word_str = self.change_syllabes(word.syll)
                word_str  = word_str.replace('-','') #word_str.split('-')

                if word.word.startswith('h') and not word.syll.startswith('8') and not word.syll.startswith('a') and not word.syll.startswith('E') :
                        word_str = 'h'+word_str
                print('before prefix', word_str)
                if not self.prefix:
                        word_str = self.prefixes(word_str, word)
                print('after prefix', word_str)
                if not self.suffix and '-' in word.syll:
                        word_str = self.real_suffixes(word_str)
                if not self.suffix:
                        word_str = self.suffixes(word_str)

                self.syllabes = [word_str]

                print('ending',self.ending)
                return Steno_Encoding(self.syllabes, self.prefix, self.suffix).encode()+self.ending


class Syllabe:
        hand = 'L'
        CONSONANTS_RHS = {
                "v": "F",
                "l": "L",
                "b": "B",
                "n": "B",
                "g": "G",
                "d": "D",
                "z": "Z",
                "k": "BG",
                "l": "FL",      # TODO When is "l" FL or L?
                "m": "PL",
                "n": "PB",      # TODO This doubles the "n" = "B" from earlier. Might be in only certain pre-defined cases like AIB = "aine"
                "Z": "G",
                "S": "FP",
                "N": "PG",
                "v": "F",
                "v": "F",

        }

        CONSONANT_PAIRS_RHS = {
                "tR": "TS",
                "st": "*S",
                "ks": "BGS",
                "bZ": "PBLG",
                "dZ": "PBLG",
                "sm": "FLP",
                "st": "*S",
                "bZ": "PBLG",
                "kR": "RBG",
                "vR": "VR",
                "fR": "VR",
                "rS": "FRPB",
                "kR": "RBG",
                "kR": "RBG",
                "kR": "RBG",
        }

        SOUNDS_RH = {
                "ST" : "TS",
                "N" : "PB",
                "M" : "PL",
                "K": "BG",
#                "L": "FL",      # TODO When is "l" FL or L?
                "N": "PB",      # TODO This doubles the "n" = "B" from earlier. Might be in only certain pre-defined cases like AIB = "aine"
#                "Z": "G",
#                "S": "FP",
#                "N": "PG",
                "V": "F",
                "I": "EU",
                "F":"FL",
                "J" : "G"

                }

        SOUNDS_LH = {
                "F" : "TP",
                "V" : "W",
                "D" : "TK",
                "I": "EU",
                "B" : "PW",
                "M" : "PH",
                "L" : "HR",
                "Y" : "KWR",
                "G" : "TKPW",
                "J" : "SKWR",
                "N" : "TPH",
                "Q" : "KW",
                "Z" : "SWR"

        }


        SOUND_RHS_EXTRA = {
                "En": "AIB",
                "wan": "OIB",

                "win": "AOUB",
                "zj§": "GZ",
                "sj§": "GZ",
                "z§": "GZ",
                "sjOn": "GZ",   # TODO This might conflict with "zj§" just above. The rule says "either `-GS/*B` or `-GZ`*
                "zjOn": "GZ",
                "@pR": "AFRPS",
                "5pR": "EUFRPS",
                "§pR": "OFRPS",
                "5sj§": "EUPBGS",    # p_incions_
                "§sj§": "OPBGS",    # pron_oncions_
                "@ksj§": "APBGS",    # san_ction_
                "5ksj§": "EUPBGS",    # dist_inction_
                "§ksj§": "OPBGS",    # j_onction_
                "ksj§": "*BGS",     # a_ction_
                "isjOn": "EUGZ",
                "tR": "TS",
                "tER": "TS",
                "tyR": "TS",
                #  "Et": "*T",      # TODO: "Et" is covered by `AIT`, I don't get this. Maybe orthographic for "ette".
                "isjOn": "EUGZ",

        }

        LEFT_KEYS = '-/*STKPWHRAO*'
        RIGHT_KEYS = '-/EU*FRPBLGTSDZ'
        consume_woyels = 'AOEU'
        keys_left = ''
        encoded_hand = ''
        already_encoded = False
        def __init__(self, syllabe, previous):
                self.previous = previous
                self.syllabe = syllabe
                self.hand = 'L'

                if (previous is not None) and previous.is_right_hand():
                        self.hand='R'

                if previous is not None:
                        self.keys_left = previous.keys_left

                if syllabe =="":
                        self.init_keys_left()
                        return None

                if self.syllabe.endswith('-'):
                        self.hand='R'
                        self.keys_left = ''
                        return None
                if self.syllabe.startswith('-'):
#                        self.hand='R'
#                        self.keys_left = ''
                        return None


                self.init_keys_left()

        def init_keys_left(self):
                self.consume_woyels = 'AOEU'
                self.keys_left = self.LEFT_KEYS
                if self.is_right_hand():
                        self.keys_left = self.RIGHT_KEYS
                return self

        def set_hand(self, hand):
                self.hand = hand
                return self
        def change_hand(self):
                if self.is_right_hand():
                        self.hand='L'
                        return self
                self.hand='R'
                return self
        
        def is_right_hand(self):
                return self.hand == 'R'

        def is_left_hand(self):
                return self.hand == 'L'

        def consume(self,syllabe, keys, sounds):
                keys = keys
                not_found = []
                rest = ''
                self.encoded_hand = ''
                print('syll',syllabe)
                print('hand',self.hand)
                for key in syllabe:
                        if not_found:
                                rest=rest+key
                                continue
                        key_trans = key
                        if not self.already_encoded and ( key in sounds.keys()):
                                key_trans = sounds[key]

                        print('key_trans', key_trans)
                        for key_trans_char in key_trans:
                                if key_trans_char in keys :
                                        keys = keys.split(key_trans_char)[1]
                                else:
                                        rest=rest+key
                                        not_found.append(key)
                                        key_trans=""
                                        break
                        if not not_found:
                                self.encoded_hand=self.encoded_hand + key_trans
                print('not_found', not_found)
                print('encoded', self.encoded_hand)
                print('rest', rest)
                self.keys_left = keys
                return (rest,not_found)
                
        def need_both_hand(self, syllabe):
                sounds = self.SOUNDS_LH
                if self.is_right_hand():
                        sounds = self.SOUNDS_RH
                print('keys_left',self.keys_left)
                return self.consume(syllabe, self.keys_left, sounds)
                
        def has_previous_R_and_L(self):
                previous = self.previous
                consume = 'R'
                while previous:
                        if previous.encoded_hand:
                                consume.replace(previous.hand, '')
                        previous = previous.previous
                return consume ==''
        def matching_syll(self, syllabe, keys) :
                for car in syllabe:
                        if car not in keys:
                                return False
                        keys = keys.replace(car,'')
                return True
                
        def encoded(self):
                piece = ""
                if self.syllabe == "":
                        return piece
                if self.syllabe.endswith('-'):
                        self.encoded_hand = self.syllabe
                        self.change_hand
                        self.keys_left=''
                        self.syllabe = self.syllabe[:-1]                    
                        return self.syllabe
                
                if self.syllabe.startswith('-'):
                        self.syllabe = self.syllabe[1:]
                        if self.syllabe.startswith('/'):
                                self.already_encoded = True
                                self.syllabe = self.syllabe[1:]          

                self.init_keys_left()


                rest = self.syllabe
                count = 1
                cpt = (self.has_previous_R_and_L())
                if (self.previous is not None) :
                        if "PBLG" in self.previous.encoded_hand:
                                self.change_hand()
                                cpt = True
                        else:
                                self.keys_left = self.previous.keys_left       
                while rest and count<30:

                        if  self.is_left_hand() and cpt:
                                cpt = False
                                piece = piece+"/"
                        (rest, not_found) = self.need_both_hand(rest)
                        piece = piece + self.encoded_hand
                        print('piece',piece)

                        if rest :
                                self.change_hand()
                                self.init_keys_left()
                                cpt = True
                        count= count +1
                        print('reste'+rest+":")
                return piece

        def replace_hand(self, syllabe, items):
                for sound in items:
                        syllabe = syllabe.replace(sound[0], sound[1])
                return syllabe

class Steno_Encoding:
        DIPHTONGS = {
                # without i
                "jEn": "AEB",
                "djO": "OD",
                "zj§": "GZ",
                "sj§": "GZ",
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                'j@' : 'AEN' , # son ian
                "RSi" : "VRPB",
                'Egze' : 'KP',
                'ijO' : 'AO',
                'Egz' : 'KP',
                "RS" : "VRPB",
                "dZ" : "PBLG",
                "bZ" : "PBLG",
                'En' : 'AIB',
                "ER" : "AIR",
#                "di" : "D",
#                "mi" : "M",
                "8i": "AU",     # pluie
                'ij': 'AO', # before jO
                'jO' : 'AO',
                "j2": "AOEU",   # vieux
                "je": "AE",     # pied
                "jE": "AE",     # ciel
                "ja": "RA",     # cria
                "jo": "RO",     # bio
#                "jO": "ROE",    # fjord # TODO unsure
                "jo": "AO",     # bio # TODO Some conflict there. "-R can be read as i" (above), but the diphtongs are more important I guess?
#                "jO": "RO",     # fjord
                "j§": "AO",     # av_ion_
                "kw": "KW",
                "wE": "WAEU",

                "wa": "OEU",    # froid
                "w5": "OEUPB",  # loin
                "wi": "AOU",    # oui
                "j5": "AEPB",   # chien
                "ey": "EU",     # r_éu_nion
                "vR": "VR",
                'oo' : 'O',    #zoo
                "ya": "WA",     # suave
#                "ij": "LZ",    # bille # TODO Maybe not a diphtong, but a word ending/consonant thing

                'fl': "FL",
                "5" : "IN",
                'u' : 'OU',

                "@": "AN",     # pluie

        }
        VOWELS = {
                "a": "A",       # chat
                "°" : "",
                'j' : 'i',
                "Z" : "G",

                "2": "AO",      # eux
                "9": "AO",      # seul
#                "E": "AEU",     # père
                "e": "E",       # clé
#                "E" : "",
                "i": "EU",      # lit
                "o": "OE",      # haut
                "O": "O",       # mort
                "y": "U",       # cru
                "u": "OU",      # mou
                "5": "EUFR",    # vin
                "8": "U",       # huit
                "§": "ON"
                # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

        }

        def __init__(self, syllabes, prefix, suffix):
                self.syllabes = syllabes
                self.prefix = prefix
                self.suffix = suffix

        def diphtongs(self, word):
                new_word=word
                for diphtong in self.DIPHTONGS.items():
                        new_word = new_word.replace(diphtong[0], "+"+diphtong[1]+"+")
                return new_word


        def force_right_hand(self, piece, previous):
                return Syllabe(piece.upper(), previous)


                
        def encode(self):
                self.word_encoded = ""
                previous = None
                if self.prefix:
                        previous = Syllabe(self.prefix, None)
                        self.word_encoded = previous.encoded()
                
                for piece in self.syllabes:
                        if piece == "":
                                continue
                        print('piece',piece)
                        piece = self.diphtongs(piece)
                        print('dif',piece)
                        piece = self.voyels(piece)
                        print('voyel',piece)
                        if piece == "":
                                continue
                        for new_piece in piece.split('+'):
                                print('syllabe',new_piece)
                                syllabe = self.force_right_hand(new_piece, previous)
                                self.word_encoded = self.word_encoded+ syllabe.encoded()
                                previous = syllabe
                        

                syllabe = self.force_right_hand(self.suffix, previous)
                self.word_encoded = self.word_encoded + syllabe.encoded()
                if self.word_encoded.startswith('/'):
                        self.word_encoded = self.word_encoded[1:]
                return  self.word_encoded

        def voyels(self, word):
                new_word=word
                for char in word:
                        if char in self.VOWELS:
                                new_word = new_word.replace(char, self.VOWELS[char])
                return new_word

