import sys
import re
class Word:
        def __init__(self, word, phonetics, lemme, cgram, genre, number, info_verb, syll):
            self.word = word
            self.phonetics = phonetics
            self.lemme = lemme
            self.cgram = cgram
            self.genre = genre
            self.number = number
            self.info_verb = info_verb
            self.syll = syll
        def __str__(self):
                print("word", self.word)
                print("phonetics", self.phonetics)
                print("lemme", self.lemme)
                print('cgram',  self.cgram)
                print('number', self.number)
                print('syll', self.syll)
                return self.syll
        def is_verb(self):
                return self.cgram == "VER"
class Steno:
        PREFIXES = {
#                "s2": "S", # ce mais pas ceux
                "@t" :"SPW",
                "5t" :"SPW",
                "e" : "",
                "tEkno" : "T",
                "tEl" : "THR-",
                "R°" : "R-",
                "S°" : "SK",
                "Sa" : "SK"
        }

        # if start with - then dont convert 
        SUFFIXES = {
                "sje" : "AE" , #caissIER
                "sjER" : "AER" , #caissiERE
                "jasm" : "-/KWRAFPL",
                "jEn": "AEB",
                "sj§" : "GS",
                "pid" : "-PD",
                "fis" : "-WEUS",
                'kE' : 'KE',
                "jER" : "AER",
                "je" : "AE",
                "jER" : "AER",
                "loZik" : "LOIK",
                "lOZist" : "-/HRO*EUS",
                "lOg" : "LO*EG",
                "d9R" : "RD",
                "dabl" : "-/TKABL",
                "abl" : "ABL",
                "jEm" : "-A*EM",
                
                "jast" : "YA*S",
                "vwaR" : "-FRS",
                "Ral" : "-RL",
                "Ribl" : "-RBL",
                "§bl": "-OFRBL",  # comble
                "@bR": "-AFRBS",   # ambre
                "5bR": "-EUFRBS",  # timbre
                "§bR": "-OFRBS",   # ombre
                "@sj§": "APBGS",    # p_ension_

                "@-S°" : "-AFRPBLG",
                "tEkt" : "-/T*K",
                "EtR" : "--TS",
                "RS" : "-FRPB",

                "@S" : "-AFRPBLG",
                "S" : "-FRPBLG",
                "m@" : "-PLT",

                "sm" : "-FPL",
                "@d" :"APBD",
                "5b": "-EUFRB",  # limbe
                "§b": "-OFRB",   # tombe
                "@bl": "-AFRBL", # tremble
                "1bl": "-EUFRBL",  # humble
                "dR" : "DZ" ,# ajoin-dre
                "@b": "-AFRB",   # jambe
                "E" : "AEU",
                "n" : "-B"

                
                
        }

        SYLLABE_PLACES = {
                "u-z" : "uz-",
                "R-Si" : "-RSi",
                "@-sj§" : "-@sj§",
                "d-ZEk": "-dZ",
                "d-Z": "-dZ",
                "S°-" : "S°",
                "vo-l": "vl-",
                "-y-" : "-y",
                "@-t" :"@t-",
                "5-t" :"5t-",
        }



        CONSONANTS_LHS = {
                "b": "PW",      # bonjour
                "d": "TK",      # dans
                "f": "TP",      # faire, phare
                "g": "TKPW",    # gare
                "k": "K",       # quoi, car
                "l": "HR",      # la
                "m": "PH",      # mais
                "n": "TPH",     # ne
                "p": "P",       # père
                "R": "R",       # rouge
                "s": "S",       # super
                "S": "SH",      # chien
                "t": "T",       # toi
                "v": "W",       # vous
                "8": "W",       # huit
                "j": "KWR",     # hier
                "z": "SWR",     # zone
                "Z": "SKWR",    # je
        }

        CONSONANT_PAIRS_LHS = {
                "gz": "KP",
                "ps": "S",
                "pn": "TPH",
                "kw": "KW",
                "tS": "SK",         # TODO: I'd rather deviate and use KH if possible
        }

        SOUNDS_LHS = {
                "de": "STK",
                "def": "STKW",
        }


        words = []
        suffix = ""
        prefix = ""
        steno_word = ""
        syllabes = []
        def __init__(self, corpus):
                self.words = corpus
                
        def find_all_same_syll(self, myword) :
                same_words = []
                for word in self.words:
                        if ((word.syll == myword.syll) and (word.word != myword.word) and not word.word.endswith('nt') and not word.word.endswith('s') and not word.word.endswith('he')):
                                same_words.append(word)
                
                for word in same_words:
                        print(word.word)
                return same_words

        def has_homophone(self, word) :
                return self.find_all_same_syll(word)
        
        def find(self,find_word):
                finds = []
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


        def prefixes(self, word):
                new_word=word
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

        def add_star(self,word):
                return word+"*"
        
        def transform(self,word):
                myword = self.find(word)
                if not myword:
                        return ""
                print(vars(myword))
                if self.has_homophone(myword) and myword.is_verb():
                        return self.add_star(self.transform_word(myword))
                myword = self.transform_word(myword)

                return myword
         
        def transform_word(self,word):
                word_str = self.change_syllabes(word.syll)
                word_str  = word_str.replace('-','') #word_str.split('-')

                if (word.word.startswith('h')):
                        word_str = 'h'+word_str

                word_str = self.prefixes(word_str)
                word_str = self.suffixes(word_str)
                self.syllabes = [word_str]
#                return Steno_Encoding(self.syllabes, self.prefix, self.suffix).encode()
                return Steno_Encoding(self.syllabes, self.prefix, self.suffix).encode()


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
                "vR": "FR",
                "fR": "FR",
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

        LEFT_KEYS = '*STKPWHRAO*'
        RIGHT_KEYS = '*EUFRPBLGTSDZ*'
        consume_woyels = 'AOEU'
        keys_left = ''
        position = 1
        encoded_hand = ''
        def __init__(self, syllabe, previous):
                self.previous = previous
                self.syllabe = syllabe
                self.hand = 'L'
                self.position = 1
                if (previous is not None) and previous.is_right_hand():
                        self.hand='R'

                if previous is not None:
                        self.position = previous.position +1
                        self.keys_left = previous.keys_left

                if syllabe =="":
                        self.init_keys_left()
                        return None

                if self.syllabe.endswith('-'):
                        self.hand='R'
                        self.position = 2
                        self.keys_left = ''
                        return None
                if self.syllabe.startswith('-'):
#                        self.hand='R'
                        self.keys_left = ''
                        return None


                self.init_keys_left()

#                if (self.both_hand):
#                        self.hand='R'
#                        self.position = self.position+1

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
#                        if self.is_left_hand() and "E" not in self.consume_woyels and "U" not in self.consume_woyels :
#                                not_found.append(key)
                        
                        if not_found:
                                rest=rest+key
                                continue
                        key_trans = key
                        if key in sounds.keys():
                                key_trans = sounds[key]
#                        if key_trans in self.consume_woyels:
#                                self.consume_woyels = self.consume_woyels.replace(key_trans,'')
#                                self.encoded_hand=self.encoded_hand + key_trans
#                                continue

                        print('key_trans', key_trans)
                        for key_trans_char in key_trans:
                                print('key_trans_char', keys)

                                if key_trans_char in keys :
                                        keys = keys.split(key_trans_char)[1]
                                        print('qui qui reste',keys)
#                                        keys = keys.replace(key_trans_char,'')
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
                
 
        def encoded(self):
                piece = ""
                if self.syllabe == "":
                        return piece
                if self.syllabe.endswith('-'):
                        self.encoded_hand = self.syllabe
                        return self.syllabe
                if self.syllabe.startswith('-'):

                        self.encoded_hand = self.syllabe[1:]

#                        if (self.previous and self.previous.is_right_hand()):

                         #       self.encoded_hand= "/"+self.encoded_hand
                        self.position = self.position + 1
                        return self.encoded_hand
                 
                self.consume_woyels = 'AOEU'
                self.init_keys_left()

                if (self.previous is not None) :
                        if "PBLG" in self.previous.encoded_hand:
                                self.change_hand()
                        else:
                                self.keys_left = self.previous.keys_left       
                #         if (self.is_right_hand()):
                #                 self.consume_woyels = self.previous.consume_woyels.replace("A","")
                #                 self.consume_woyels = self.consume_woyels.replace("O","")               
                #         else:
                #                 self.consume_woyels = self.previous.consume_woyels.replace("E","")
                 #               self.consume_woyels = self.consume_woyels.replace("O","")               
                 



                rest = self.syllabe
                count = 1
                cpt = (self.previous and self.previous.encoded_hand and self.position > 3)
                while rest and count<30:

                        if  self.is_left_hand() and cpt :
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
                        self.position = self.position +1 
                        print('reste'+rest+":")
                return piece
#                   print('left_hand',piece+self.replace_hand(self.syllabe,self.SOUNDS_LH.items()))
#                        return piece+self.replace_hand(self.syllabe,self.SOUNDS_LH.items())

        def replace_hand(self, syllabe, items):
                for sound in items:
                        syllabe = syllabe.replace(sound[0], sound[1])
                return syllabe

class Steno_Encoding:
        DIPHTONGS = {
                # without i
                "jEn": "AEB",
                "djO": "OD",
                "RSi" : "VRPB",
                "RS" : "VRPB",
                "dZ" : "PBLG",
                "di" : "D",
                "mi" : "M",
                "8i": "AU",     # pluie
                "j2": "AOEU",   # vieux
                "je": "AE",     # pied
                "ja": "RA",     # cria
                "jo": "RO",     # bio
                "jO": "ROE",    # fjord # TODO unsure
                "jo": "AO",     # bio # TODO Some conflict there. "-R can be read as i" (above), but the diphtongs are more important I guess?
                "jO": "AO",     # fjord
                "j§": "AO",     # av_ion_
                "wa": "OEU",    # froid
                "w5": "OEUPB",  # loin
                "wi": "AOU",    # oui
                "j5": "AEPB",   # chien
                "ey": "EU",     # r_éu_nion
                "vR": "FR",
                "ya": "WA",     # suave
                "ij": "LZ",    # bille # TODO Maybe not a diphtong, but a word ending/consonant thing
                "@": "AN",     # pluie
        }
        VOWELS = {
                "a": "A",       # chat
                "°" : "",
                "Z" : "G",
                "e": "E",       # clé
                "2": "AO",      # eux
                "9": "AO",      # seul
             #  "E": "AEU",     # père
#                "E" : "",
                "i": "EU",      # lit
                "o": "OE",      # haut
                "O": "O",       # mort
                "y": "U",       # cru
                "u": "OU",      # mou
                "5": "EUFR",    # vin
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
