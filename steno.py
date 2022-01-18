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
#                return 'par' in self.info_verb and
                return self.is_verb() and self.word.endswith('ant')

        def is_vous_ind_present(self):
                return 'ind' in self.info_verb and self.word.endswith('ez')

        def is_plural(self) :
                return self.number =='p'

class Ortho:

        sounds = ''
        sound = ''
        replace_by = ''
        steno_str =''
        prefix = False
        check_alternative = False
        alternative_str = ''
        one_hand = False
        converted_syll = False
        def __new__(cls,sound, replace_by):
                return super().__new__(cls)
        
        def __init__(self,sound,replace_by):
                self.converted_syll = False
                self.sounds = sound.split('|')
                self.replace_by = replace_by

        def steno(self):
                return self.steno_str
        
        def one_hand(self):
                self.one_hand = True
                return self
                
        def matches(self,word, pattern) :
                return  word.word.endswith(pattern)

        def alternative(self, string) :
                self.check_alternative = True
                self.alternative_str = string
                return self

        def get_alternative_str(self, word, suffix_str) :
                return word.replace(suffix_str, self.alternative_str)

class Log:
        activate = True
        def __init__(self, message, value = '') :
                if self.activate: 
                        print(message, value)

class OrthoSuffix(Ortho):
        
        def convert(self,word) :
                for sound in self.sounds:
                        if word.syll.endswith(sound) :
                                word.syll = word.syll[:-len(sound)]
                                self.steno_str = self.replace_by
                                Log('ortho suffix convert',word.syll)
                                return word
                return False

        def can_be_converted(self, word):
                for sound in self.sounds:
                        if word.syll.endswith(sound) :
                                self.sound = sound
                                return True
                                
                return False

class OrthoPrefix(Ortho):
        def convert(self,word):
                for sound in self.sounds:

                        if word.syll.startswith(sound) :
                                word.syll = word.syll[len(sound):]
                                self.steno_str = self.replace_by
                                Log('ortho prefix convert',word.syll)
                                return word
                return False

        def can_be_converted(self, word):
                Log('self sounds', self.sounds)
                Log('word', word)
                for sound in self.sounds:
                        if word.syll.startswith(sound) :
                                self.sound = sound
                                return True
                Log('cant be converted ')
                return False
class Steno:
        PREFIXES = {
#                "s2": "S", # ce mais pas ceux
                "sypER" : "SP-R/",
                "tEkno" : "T",
                "tR@s" : "TRAPBS/",
                "tR@z" : "TRAPBS/",
                "tEl" : "THR-",
                'Eksp' : "-/BGSP",
                'Ekst' : "-/BGST",
                'EksK' : "-/BGST",
                'ade' : 'ATK', # sound
                'm°n' : "KH",#men
                'min' : "KH",#min
                'm2n' : 'KH', #men
                't°n' : 'TH', #tenace
                'ten' : 'TH', #tenace
                'ina' : 'TPHA',
                'inE' : 'TPHAEU',
                'ini' : 'TPHEU',
                'in§' : 'TPHOPB',
                'ino' : 'TPHO',
                'iny' : 'TPHU',
                '5sy' : 'STPHU',
                '5si' : 'STPHEU',
                '5sa' : 'STPHA',
                '5se' : 'STPHE',
                '5k' : '/EUFRPB',
                "kR" : "KR", #craquait
                "S°" : "SK",
                "@t" :"SPW",
                "5t" :"SPW",
                "R°" : "R",
                "Z°" : "SKW-", #gelé
#                "gl" : "
                "Sa" : "SK",
                'ke' : 'K',
                'dR' : 'TKR',
                'sin' : 'STPH',
                'sn' : 'STPH',
#                'k§' : '-KON', # conte
                'k§' : 'KOEPB', # content
                'du' : 'TKOU',
                "pn" : "TPH",
                "@p" : "KPW",
                "5p" : "KPW",
                "@b" : "KPW",
                "5b" : "KPW",
                "tR": "TR", #trappeur
                'S' : 'SH',
#                "e" : "",
#                'ad' : 'A-D', # sound 
                "Z" : "SKWR",
#                'd' : 'DAOE',
                'z' : 'Z',
                'a':'A|AE/',
                
        }

        ORTHO_PREFIXES = {
                'multi' :OrthoPrefix('myl-ti', 'PHULT'),
                'corr' : OrthoPrefix('ko-R', 'KR'),
                'coll' : OrthoPrefix('ko-l', 'KHR'),
                "comm" : OrthoPrefix('ko-m|kOm','KPH'),
                "com" : OrthoPrefix('k§','K*/|K'),
                "con" : OrthoPrefix('k§','KOEPB|KOPB'),
                'ind' : OrthoPrefix('5-d', 'SPW'),
                'end' : OrthoPrefix('@-d', 'SPW'),
                'réu' : OrthoPrefix('Re-y', 'REU'),
                'fin'  : OrthoPrefix('fi-n', 'WH'),
                'fen'  :OrthoPrefix('f°-n', 'WH'),
                
#                "a" : OrthoPrefix('a-','AE-'), # sound

                }

        
        ORTHO_SUFFIXES = {
                'cation' : OrthoSuffix('ka-sj§','-BGS'),

                'lation' : OrthoSuffix('la-sj§', '-/LGS'),
                'bilité' : OrthoSuffix('bi-li-te','-BLT'),
                'ilité' : OrthoSuffix('i-li-te','ILT'),
                'lité' : OrthoSuffix('li-te','-LT'),
                'bilise' : OrthoSuffix('bi-liz','-BLZ'),
                'ralise' : OrthoSuffix('Ra-liz','-BLZ'),
                'lise' : OrthoSuffix('liz','-LZ'),

                'rité' : OrthoSuffix('Ri-te', '-RT'), # securite
                'bité' : OrthoSuffix('bi-te','-BT'),
                'tivité': OrthoSuffix('ti-vi-te', '-/TEUFT'),
                'vité': OrthoSuffix('vi-te', '-/FT'),
                'cité': OrthoSuffix('si-te', '-/FT'),
                'sité': OrthoSuffix('si-te', '-ST*E'),
                'igé': OrthoSuffix('i-Ze', 'EG'),
                'iger': OrthoSuffix('i-ZeR', '-*EG'),
                'ience' : OrthoSuffix('j@s', '-AENS'),
                'ance' : OrthoSuffix('@s', '-NS'),
                'ence' : OrthoSuffix('@s', '-NS'),
                'ande' : OrthoSuffix('@d', '-ND'),
                'aux' : OrthoSuffix('o', '-O*EX'),
                'ité' : OrthoSuffix('i-te','ITD'),
                'gueur' : OrthoSuffix('g9R' , '-RG'),
                'deur' : OrthoSuffix('d9R' , '-RD'),
                'lheur' : OrthoSuffix('l9R' , '-RL'),
                'leur' : OrthoSuffix('l9R' , '-RL'),
                "cteur" : OrthoSuffix("k-t9R", "-RT") ,
                "teur" : OrthoSuffix("t9R", "-/RT") ,

                "nheur" : OrthoSuffix("n9R", "-RN") ,
                "neur" : OrthoSuffix("n9R", "-RN") ,
                "rtion" : OrthoSuffix("R-sj§", "-RGS"),
                "ration" : OrthoSuffix("Ra-sj§", "-RGS"),
                "trice" : OrthoSuffix("tRis", "-/RTS") ,
                'cienne' : OrthoSuffix('sjEn', '-GZ'),
                "telle" : OrthoSuffix("tEl" , "-/LGTS"),
                "tel" : OrthoSuffix("tEl" , "-/LGTS"),
                "velle" : OrthoSuffix("vEl", "-/FL"),
                "quelle" : OrthoSuffix("kEl", "-/BLG"),
                "quel" : OrthoSuffix("kEl", "-/BLG"),
                "elle" : OrthoSuffix("El", "-/*EL"),
                "ière"  : OrthoSuffix('jER', 'A*ER'),
                "ier"  : OrthoSuffix('je', 'AER'),
                'ive' : OrthoSuffix('i-v|i-ve|iv', '-/*EUF'),
                'if' : OrthoSuffix('if', '-/*EUFL'),
                'cien' : OrthoSuffix('sj5', '-GS'),
                "ain" : OrthoSuffix("5", "IN"),
                'cte' : OrthoSuffix('kt', 'KT'),
                "ène" : OrthoSuffix("En","-/*EB"),
#                "eur" : OrthoSuffix("9R","-AO*R"),
                "uel" : OrthoSuffix("y-El","-/U*EL"),
                "uel" : OrthoSuffix("8El","-/W*EL"),
                "anche" : OrthoSuffix("@S","-/AFRPBLG"),
                "rche" : OrthoSuffix("RS","-/FRPB"),
                "che" : OrthoSuffix("S","-/FP"),
                "ué" : OrthoSuffix("8e","-/W*E"),
                "cise" :OrthoSuffix("siz", "-/RBZ"),
                "cis" :OrthoSuffix("si", "-/RB"),

                "ssis" :OrthoSuffix("si", "-/RB"),
                "ci" : OrthoSuffix("si", "-/RB"),
                "cet" : OrthoSuffix("sE", "-SZAEU"),
                "ce" : OrthoSuffix("s", "-SZ").alternative('ss'),
                "el" : OrthoSuffix("El", "-/*EL"),
                "th" : OrthoSuffix("t", "-GT"),
                "the" : OrthoSuffix("t", "-GT"),
                "a" : OrthoSuffix("a", "-/*Z"),
                

        }
                

        REAL_SUFFIXES = {
                "En" : "A*IB",
                
                "wE": "-/W*E",


        }

        # if start with - then dont convert 
        SUFFIXES = {
                'pasj§' :  '-PGS', # preocuppation
                't82' : '-/TWAO*', # fru-ctu-eux
                'sjasj§': 'SRAGS', #ciation
                '@sjOn' : "ANGZ", #mentionne
                '5ksj§' : "PBGS", #distinction
                '§ksjOn' : "-/OPBGS/*B", #fo-nctionne
                'ksj§' : "*BGS", #friction
                "zj§": "-GZ",
                "vwaR" : "-/FRS",
                "val" : "-/FL",
                "vaj" : "-/FL",
                "vEl" : "-/FL",
                'Rnal' :'-RBL',
                'sjOn' :'-GZ',
                't8ER' : 'TW*R', # portuaire
                'tyR' : '-TS', #ture
                '@gl' : '-/AFRLG',
                '§gl' : '-/OFRLG',
                '5gl' : '-/EUFRLG',
                'nal' : '-NL', #canal



#second option                'sjOn' :'-/GS/*B',
                "tER": "-TS",  #notaire
                "EtR" : "-TS" , #fenetre
                "jEm" : "-/A*EPL",
#                "jER" : "AER" , #caissiERE
                "jasm" : "-/KWRAFPL",
                "jEn": "AEB",
                "sj§" : "GS",
                "loZik" : "LOIK",
                "lOZist" : "-/HRO*EUS",
                "lOZi" : "LO*IG",
                "lOg" : "LO*EG",
                "p9R" : "-RP",
                "pid" : "-PD",
                "fis" : "-WEUS",
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                "kEl" : "-/BLG",
                "§kl" : "-/OFRBLG", # oncle
                "akl" : "-/AFRBLG", 
#                "je" : "AER" , #caissIER

#                "l9R" : "-RL",
#                "d9R" : "RD",
                "dabl" : "-/TKABL",
                "v°m@" : "-/FPLT",
                "@sj§": "APBGS",    # p_ension_
                "jast" : "YA*S",
                "vwaR" : "-/FRS",

                "Ribl" : "-RBL",
                "@tR" : "-NTS", #-ntre
                "stR" : "-TS", #-stre
                "RtR" : "-RTS", #-rtre
                "§pR" : '-/OFRPS',
                "@b": "-/AFRBL",   # tremble
                "§bl": "-/OFRBL",  # comble
                "1bl": "-/UFRBL",  # comble
                "@bR": "-/AFRBS",   # ambre
                "5bR": "-/EUFRBS",  # timbre
                "§bR": "-/OFRBS",   # ombre
                "5b": "-EUFRB",  # limbe
                "§b": "-/OFRB",  # comble
                "ks": "-BGS",
                "t@" : "/TAPB", #content
                "ve": "-WE", # releve
                "N§" : "-/HO*PB", #bourguignon
                "@Z" :"-/APBLG", # ange
                "5Z" :"-/EUPBLG", # linge
                "§t" : "-/OFRPT", # prompte
                "5p" : "-/EUFRP",
                '@pl' : "-/AFRPL",
                "9R":"-AO*R",
                '@p' : '-/AFRP' , #campe
                '§p' : '-/OFRP', # trompe
                'Ribl' : '-RBL',
                'Rbal' : '-RBL' , #verbal
                'bal' : '-BR' , #global
                "Ral" : "-RL",
                'kE' : 'KE',
                'vERs' : '-/FRBS', # diverses
                'ERv' : '-/FRB', #v-erve
                'vEr' : '-/FRB', # cou-vert
                'vER' : '-/FRB', # travers
                'REj' : '-RLZ' , #reille
                
#                'fER' : '-/FRB', #o-ffert
                'fER' : '-/FR', #faire
                'vR' : '-/FR', # iv-re
                'fR' : '-/FR' , #sou-fre
                '@l' : '-ANL', #branle
                'zm' : '-/FPL',
                'sm' : '-/FPL',
                'di' : '-/*D',  #interdit ?
                "tEkt" : "-/T*K",
                "EtR" : "-TS",
                "SEt" : "-/FPT" , # achete
#                "RZ" : "-/RPBLG",
                "RZ" : "RG",
                "bl" : "-BL",
                "@S°" : "-AFRPBLG",
                "fR" : "-/FR", #souffre
                "fl" : "-/FL", #souffle
                'sk°'  : '-/FBG', #puisque
                'sk' : '-/FBG',

                "Re":"-/R*E|-RE",
                'z§':'-GZ',
                "@S" : "-AFRPBLG",
                "st" : "-*S",
                "ZE" : "G",
                'ij' : '-LZ', #ille

                "S" : "-/FRPBLG",
                "m@" : "-/PLT",
                "En" : "AIB",
                "ER" : "AIR",
                "@d" :"PBD",

                "dR" : "DZ" ,# ajoin-dre
                "@b": "-AFRB",   # jambe
                "tR": "-TS", #tre - 
                "bR":"-BS",  #-bre
                "pR":"-PS", #-pre
                "nEs" : "BS",
                "Et" : "AEUT",
                "E" : "AEU",
                "e" : "AEU",
                "n" : "B",
                'j' : '-LZ',
                "§" : "-*PB",
#                "sm" : "-/FP",
                'o' : 'OE',
#                't' : 'T',
                'N' : 'PG',
                'El' :'-FL',
                "Z" : "G", # rage
                'u' : 'O*U',
                'k' : 'K',

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
                'de' : 'd',

        }


        words = []
        suffix = ""
        prefix = ""
        steno_word = ""
        syllabes = []
        ending = ""
        homophones = False
        pronoun = ""
        final_encoded = []
        ending_syll = ''
        force_verb = False
        force_noun = False
        def __init__(self, corpus):
                
                self.suffix = ""
                self.prefix = ""
                self.steno_word = ""
                self.syllabes = []
                self.ending = ""
                self.homophones = False
                self.pronoun = ""
                self.ending_syll = ''
                self.suffix = ''
                self.final_encoded = []
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
                        Log(word.word)
                self.homophones = same_words
                return same_words

        def find_same_word_verb(self, myword) :
                if not self.force_verb:
                        return myword
                same_words = []
                for word in self.words:
                        if word.word == myword.word and word.is_verb():
                                return word
                return myword

        def find_same_word_not_verb(self, myword) :
                if not self.force_noun:
                        return myword
                same_words = []
                for word in self.words:
                        if word.word == myword.word and not word.is_verb():
                                return word
                return myword

        def find_spelled_word(self,string):
                for word in self.words:
                        if word.word==string:
                                return word
                return False
                        

        def remove_last_syll(self, syll):
                sylls = syll.split('-')
                sylls.pop()
                return "-".join(sylls)

        # def orth_ending_iere(self,word, pattern):
        #         if word.endswith('ière'):
        #                 return pattern.replace('AER', 'A*ER')
        #         if words.endswith('ier') and not pattern.endswith('R'):
        #                 return pattern+'R'
        #         return pattern

        def orth_write_ending_d(self,word):
                if word.word.endswith('d') and self.has_homophone(word):
                        self.ending = 'D'
                return word

        def ortho_starting_with_des(self,myword):
                word = myword
                syll = word.syll.replace('-','')
                Log('sp', syll)
#                if not syll.startswith('dez') and not syll.startswith('des') and not syll.startswith('d°s'):
                if not word.word.startswith('de') and not word.word.startswith('dé'):
                        return word
                next_letter = word.word[:4].upper()
                Log('next letter', next_letter)
                if word.word.startswith('dé') or ((next_letter.endswith('O') or next_letter.endswith('E') or next_letter.endswith('I') or next_letter.endswith('A') or next_letter.endswith('U') or next_letter.endswith('@') or next_letter.endswith('Y'))) :
                        
                        if 'de-z' in word.syll:
                                self.prefix = {'STK':'dez'}
                                word.syll = word.syll.replace('de-z', '')
                        if 'de-s' in word.syll:
                                self.prefix = {'STK':'des'}
                                word.syll = word.syll.replace('de-s', '')
                        if 'd°-z' in word.syll:
                                self.prefix = {'STK':'d°s'}                                
                                word.syll = word.syll.replace('d°-s', '')
                        if (word.syll.startswith('de-f')):
                                self.prefix = {'STKW' : 'def'}
                                
                                word.syll = word.syll.replace('de-f', '')
                        word.syll = word.syll.replace('de', '')
                        Log('syll repl', word.syll)
                
                return word
                
        def ortho_add_aloneR_infinitif_firstgroup(self, word):
                verb_word = self.find_same_word_verb(word)
                if verb_word.is_verb() and verb_word.is_infinitif()  and verb_word.word.endswith('er'):
                        self.ending = "/-R"
                        if verb_word.syll.endswith('e') :
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word
                return word

        def ortho_add_alone_keys_on_noun(self,word):
                if word.is_verb():
                        return word
                if word.word.endswith('ette'):
                        self.ending = "/*T"
                        if word.syll.endswith('Et') :
                                Log('fini par et')
                                self.ending_syll = word.syll[:-2]
                        return word
                return word

        def ortho_suffixes(self,word):
                for orth in self.ORTHO_SUFFIXES.items():
                        if word.word.endswith(orth[0]) :
                                ortho = orth[1]

                                if ortho.check_alternative :
                                        if not self.find_spelled_word(ortho.get_alternative_str(word.word,orth[0])):
                                                Log('cotinue check alternative')
                                                continue
                                Log(vars(ortho))
                                Log(vars(word))
                                Log('can be' , ortho.can_be_converted(word))
                                if (ortho.can_be_converted(word)):
                                        myword = ortho.convert(word)
                                        Log('converted ok',myword)
                                                                                
                                        self.suffix = ortho.steno()
                                        return myword
                return word

        def ortho_prefixes(self,word):
                Log('ortho_prefixes start')
                for orth in self.ORTHO_PREFIXES.items():
                        Log('word',word.word)
                        if word.word.startswith(orth[0]):
                                Log(vars(orth[1]))
                                ortho = orth[1]
                                ortho.prefix = True

                                if (ortho.can_be_converted(word)):
                                        myword = ortho.convert(word)
                                        self.prefix = {ortho.steno() : ortho.sound}
                                        Log('prefix test' , self.prefix)
                                        return myword
                return word

        
        def ortho_add_alone_keys_on_verb(self,word):
                verb_word = self.find_same_word_verb(word)

                if not verb_word.is_verb():
                        return word
                if  verb_word.is_passe_compose():
                        if verb_word.syll.endswith('ué') :
                                self.ending = "/W*E"
                                self.ending_syll = verb_word.syll[:-2]
                                return verb_word
                        if verb_word.syll.endswith('e') :
                                self.ending = "/-D"
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word

                if verb_word.is_imparfait():
                        self.ending = "/-S"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word

                if verb_word.is_conditionnel():
                        self.ending = "/-RS"
                        if verb_word.word.endswith('rrait') and verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                                return verb_word
                        if verb_word.syll.endswith('RE') :
                                self.ending_syll = verb_word.syll[:-2]
                        return verb_word

                if verb_word.is_vous_ind_present():
                        self.ending = "/*EZ"

                        if verb_word.syll.endswith('Re') :
                                Log('indic')
                                self.ending = "/R*EZ"
                                self.ending_syll = verb_word.syll[:-2]
                                return verb_word
                        if verb_word.syll.endswith('e') :
                                self.ending_syll = verb_word.syll[:-1]
                                return verb_word
                if verb_word.is_participe_present():
                        Log('participe present')
                        self.ending = "/-G"
                        if verb_word.syll.endswith('j@')  :
                                self.ending_syll = verb_word.syll[:-2]
                                return verb_word
                        if verb_word.syll.endswith('@') :
                                self.ending_syll = verb_word.syll[:-1]
                                return verb_word
                        return verb_word
                
                return word
                
        def try_to_remove_woyel(self, myword) :
                sylls = myword.syll
                same_words=[]
                Log('remove last syll',self.remove_last_syll(sylls))
                Log('number of i ',len(myword.word.split('i')))
                if ('8i' in self.remove_last_syll(sylls)) or ('i' not in self.remove_last_syll(sylls)) or (len(myword.syll.split('i'))<3):
                        return myword.syll

                sylls = sylls.replace('i','',1)
                        
                for word in self.words:
                        if (self.ortho_ending(word.word, myword.word) and (word.syll.replace('i','',1)==sylls or word.syll.replace('e','',1)==sylls)):
                        #or word.syll.replace('E','',1)==sylls)):
                                same_words.append(word)

                for word in same_words:
                        Log('found word same vowel:',word.word)
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
                                return copy.copy(find_word)

                if finds:
                        return copy.copy(finds[0])
                return False

        def change_syllabes(self, word):
                new_word=word
                for syll in self.SYLLABE_PLACES.items():
                        new_word = new_word.replace(syll[0], syll[1])
                return new_word


        def prefixes(self, word, word_class):
                if (word_class.word.startswith('y') and word.startswith('j')):
                        self.prefix ={'KWR' : 'j'}
                        new_word = word.replace('j','',1)
                        return new_word
                
                new_word=word
                if  self.pronoun:
                        self.prefix={'Y': 'y'}
                        return word
                for prefix in  self.PREFIXES.items():
                        if len(re.split("^"+prefix[0], new_word))>1:
                                self.prefix = {prefix[1] : prefix[0]}
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

        
        def double_consonant_remove_woyel(self,word,syll):
                DOUBLE_CONS = {
                        'ell' :'El|el',

                        'eill': 'Ej',
                        'ill': 'ij',
                        'ill': 'il',
                        'all' : 'al',
                        'err'  :'ER|eR',
                        'urr' : 'uR'

                }
                Log('double consonant', word)
                Log('double consonant', syll)
                for elem in DOUBLE_CONS.items() :
                        alpha = elem[0]
                        splitted = elem[1].split('|')
                        for sound in splitted:
                                Log('sound',sound)
                                if alpha in word and  sound in syll :

                                        Log('double syll',sound[1:])
                                        syll = syll.replace(sound, sound[1:])
                                        Log('double syll',syll)
                                        return syll
                return syll

        
        def add_star(self,word):
                if (self.ending):
                        return word

                Log('add star', word)                
                if ('*' in word):
                        return word
                splitted = word.split('E')
                if len( splitted) > 1:
                         splitted[len(splitted)-2] = splitted[len(splitted)-2]+"*"
                         return 'E'.join(splitted)
                splitted = word.split('U')
                Log('add star', word)                
                if len( splitted) > 1:
                         splitted[len(splitted)-2] = splitted[len(splitted)-2]+"*"
                         return 'U'.join(splitted)
                splitted = word.split('O')
                if len( splitted) > 1:
                         splitted[len(splitted)-1] = "*"+splitted[len(splitted)-1]
                         return 'O'.join(splitted)

                splitted = word.split('A')
                if len( splitted) > 1:
                         splitted[len(splitted)-1] = "*"+splitted[len(splitted)-1]
                         Log('splitted "A"',splitted)
                         return 'A'.join(splitted)
                
                return word+"*"
        
        def transform(self,word):
                                


                self.final_encoded = []
                myword = self.find(word)
                if not myword:
                        return ""
                Log(vars(myword))
#                myword.syll = self.try_to_remove_woyel(myword)
#                self.prefix ={}
#                self.suffix =""
                self.transform_word(myword)
                Log('is verb' , myword.is_verb())
                has_homophone = self.has_homophone(myword)
                Log('has homophone' , has_homophone)
                finals = self.final_encoded
                Log('final_encoded' , self.final_encoded)
                return self.final_encoded

        def prefix_h(self, word, syll) :
              
                if word.startswith('h') and not syll.startswith('8') and not syll.startswith('a') and not syll.startswith('E') and not syll.startswith('1') :
                        return 'H'
                return ''
        
        def get_prefix_and_suffix(self, initial_word, check_prefix = True, check_suffix = True ) :
                Log('Get prefi and suffix', initial_word)
                word = initial_word
                self.prefix ={}
                
                self.suffix =""
                if check_prefix:
#                        self.orth_write_ending_d(word)
                        word = self.ortho_prefixes(word)
                if check_suffix:
                        word = self.ortho_suffixes(word)
                        Log('suffix', self.suffix)
                        word = self.ortho_add_aloneR_infinitif_firstgroup(word)
                        word = self.ortho_add_alone_keys_on_verb(word)
                        word = self.ortho_add_alone_keys_on_noun(word)
                if check_prefix and not self.prefix:
                        word = self.ortho_starting_with_des(word)
                Log('suffix', self.suffix)
                word_str = self.change_syllabes(word.syll)
                word_str  = word_str.replace('-','') #word_str.split('-')
                word_str = self.prefix_h(word.word, word.syll)+word_str

                Log('self prefix', self.prefix)                        
                Log('before prefix', word_str)
                if check_prefix and not self.prefix:
                        word_str = self.prefixes(word_str, word)
                Log('after prefix', word_str)
                Log('suffix', self.suffix)

                if check_suffix and (not self.suffix and '-' in word.syll):
                        word_str = self.real_suffixes(word_str)
                if check_suffix and not self.suffix:
                        word_str = self.suffixes(word_str)
                Log('suffix', self.suffix)

                return word_str

        def transform_word(self,initial_word):
                myinitial_word= copy.copy(initial_word)
                all_sylls = initial_word.syll.replace('-','')
                all_sylls = self.double_consonant_remove_woyel(initial_word.word, all_sylls)
                all_sylls =[all_sylls]
                if myinitial_word.is_plural() and myinitial_word.word.endswith('s'):
                        return []

                word_str = self.get_prefix_and_suffix(myinitial_word)
                
                self.syllabes = [word_str]
                Log('syllabe',self.syllabes)
                Log('ending',self.ending)
                Log('ending_syll',self.ending_syll)

                for aprefix, phonem  in self.prefix.items():
                        for  one_prefix in aprefix.split('|'):
                                if not self.ending: 
                                        self.final_encoded.append(Steno_Encoding(self.syllabes, one_prefix, self.suffix.split('|')[0]).encode())

                                if self.ending :
                                        myendingword =  initial_word
                                        myendingword.syll= self.ending_syll
                                        word_str = self.get_prefix_and_suffix(myendingword,True,True)
                                        Log('endi : ',word_str)
                                        suff = ""
                                        Log('suffix endi', suff)
#                                self.syllabes = [word_str]
#                                self.prefixes(self.ending_syll, word)
#                                suff =self.suffix.split('|')[0]


                                        self.final_encoded.append(Steno_Encoding(re.sub( "^"+ phonem, '', self.ending_syll).split('-'), one_prefix, suff).encode()+self.ending)

#                word_str = self.get_prefix_and_suffix(initial_word)
#                self.syllabes = [word_str]

                for  one_suffix in self.suffix.split('|'):
                        prefix = ""
                        if self.prefix: 
                                prefix = list(self.prefix.keys())[0].split('|')[0]
                        if not self.ending :
                                self.final_encoded.append(Steno_Encoding(self.syllabes, prefix, one_suffix).encode())
#                        if self.ending :
#                                word_str = self.get_prefix_and_suffix(initial_word,True,False)
#                                word_str = self.get_prefix_and_suffix(initial_word,True,False)
#                                suffix ='' 
#                                self.final_encoded.append(Steno_Encoding([self.ending_syll.replace('-', '')], self.prefix.split('|')[0], self.suffix).encode()+self.ending)



                self.prefix ={}
                word_str = self.get_prefix_and_suffix(initial_word,True,False)
                if self.ending_syll:
                        Log('ending_syll:' , self.ending_syll)
                if self.ending :
                        encoded_w = Steno_Encoding([self.ending_syll.replace('-', '')], "","").encode()+self.ending
                        Log('ending encoding: ', encoded_w)
                        self.final_encoded.append(encoded_w)



                
                Log('> syl',initial_word.syll)
                if not self.ending :
                        self.final_encoded.append(Steno_Encoding(all_sylls, '', '').encode())
                has_homophone = self.has_homophone(initial_word)
                for final_word in  self.final_encoded:
                                                
                        Log('final_word' , final_word)
                        self.final_encoded.remove(final_word)
                        if has_homophone and initial_word.is_verb():
                                final_word = self.add_star(final_word)
#                        final_word = self.orth_ending_iere(initial_word.word, final_word)
                        
                        Log('final_word' , final_word)
                        self.final_encoded.append(final_word)

                return self.final_encoded
        


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
                "J" : "G",
                'X' : 'BGS',

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
                'X' : 'KP',

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
        RIGHT_KEYS = '-/*EUFRPBLGTSDZ'
        consume_woyels = 'AOEU'
        keys_left = ''
        encoded_hand = ''
        already_encoded = False
        next_sylls = []
        one_hand = False
        is_prefix = False
        is_suffix = False
        def __init__(self, syllabe, previous, next_sylls):
                self.previous = previous
                self.syllabe = syllabe
                self.hand = 'L'
                self.next_sylls = next_sylls
                if (previous is not None) and previous.is_right_hand():
                        self.hand='R'

                if previous is not None:
                        self.keys_left = previous.keys_left

                if syllabe =="":
                        self.init_keys_left()
                        return None

                if self.syllabe.endswith('-'):
#                        self.hand='R'
                        self.keys_left = ''
                        return None
                if self.syllabe.startswith('-'):
#                        self.hand='R'
#                        self.keys_left = ''
                        return None


                self.init_keys_left()

        def set_one_hand(self):
                self.one_hand = True
                return self
        
        def prefix(self):
                self.is_prefix = True
                return self

        def suffix(self):
                self.is_suffix = True
                return self

        
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
                        Log('change_hand to Gauche')
                        self.init_keys_left()
                        return self
                self.hand='R'
                Log('change_hand to droite')
                self.init_keys_left()
                return self
        
        def is_right_hand(self):
                return self.hand == 'R'

        def is_left_hand(self):
                return self.hand == 'L'

        def contains_woyels(self, word) :
                return "*" in word or "A" in word or "O" in word or "E" in word or "U" in word
                
        def add_hyphen(self, word):

                if self.already_encoded :
                        return word
                Log('hand', self.hand)
                Log('word', word)
                if self.previous is None and self.hand == 'R'  and self.already_encoded == "" :
                        return '-'+word
                
                if self.previous is None :
                        return word
                previous_encoded = self.previous.encoded_hand
                if (self.encoded_hand != '') :
                        previous_encoded = previous_encoded + self.encoded_hand
                if self.previous is not None:
                        Log('add hyphen previous encod',previous_encoded)

                if not (self.hand == 'R' and (self.previous.hand == 'L')):
                        return word

                if  self.contains_woyels( previous_encoded) or self.contains_woyels(word):
                        return word

                Log('added hyphen to word',word)

                return "-"+word
                
        def consume(self,syllabe, keys, sounds):
                keys = keys
                not_found = []
                rest = ''
#                self.encoded_hand = ''
                Log('syll',syllabe)
                Log('hand',self.hand)
                Log('already_encoded',self.already_encoded)
                Log('keys left',keys)
                if ("|" in syllabe) :
                        syllabe_split = syllabe.split('|')[0]
                        if self.is_right_hand() and len(syllabe.split('|'))>1:
                                syllabe_split = syllabe.split('|')[1]
                        if not self.syll_can_enter(syllabe_split, keys):
                                self.change_hand()
                                keys =self.keys_left
                                sounds = self.SOUNDS_LH
                                if self.is_right_hand() :
                                        sounds = self.SOUNDS_RH
                                syllabe_split = syllabe.split('|')[0]
                                if self.is_right_hand() and len(syllabe.split('|'))>1:
                                        syllabe_split = syllabe.split('|')[1]
                        syllabe = syllabe_split

                if (self.already_encoded and self.previous):
                        if  not self.contains_woyels( self.previous.encoded_hand) and not self.contains_woyels(self.syllabe) and '-' not in self.encoded_hand:
                                self.encoded_hand =self.encoded_hand+ '-'
                Log('keys left',keys)
                for key in syllabe:
                        if not_found:
                                rest=rest+key
                                continue
                        key_trans = key
                        if not self.already_encoded and ( key in sounds.keys()):
                                key_trans = sounds[key]

                        Log('key_trans', key_trans)
                        for key_trans_char in key_trans:
                                if key_trans_char in keys :
                                        keys = keys.split(key_trans_char)[1]
                                else:
                                        rest=rest+key
                                        not_found.append(key)
                                        key_trans=""
                                        break
                                
                        if not not_found:
                                self.encoded_hand = self.encoded_hand + self.add_hyphen(key_trans)
#                                self.encoded_hand=self.encoded_hand + key_trans

                Log('not_found', not_found)
                Log('encoded', self.encoded_hand)
                Log('rest', rest)
                self.keys_left = keys
                return (rest,not_found)
                
        def consume_syll(self, syllabe):
                sounds = self.SOUNDS_LH
                if self.is_right_hand():
                        sounds = self.SOUNDS_RH
                Log('keys_left',self.keys_left)
                return self.consume(syllabe, self.keys_left, sounds)
                
        def has_previous_R_and_L(self):
                previous = self.previous
                consume = 'R'
                while previous:
                        if previous.encoded_hand:
                                consume.replace(previous.hand, '')
                        previous = previous.previous
                return consume ==''
        def syll_can_enter(self, syll, keysleft) :
                for char in syll:
                        if not char in keysleft:
                                Log('have to change')
                                return False
                        keysleft = keysleft.split(char)[1]
                return True
        def get_hand_sound(self, hand, syllabe ,already_encoded):
                
                not_found = []
                rest = ''
                sounds = self.SOUNDS_LH
                keys = self.LEFT_KEYS
                encoded = ''
                if hand == 'R':
                        keys = self.RIGHT_KEYS
                        sounds = self.SOUNDS_RH
                if ("|" in syllabe) :
                        syllabe = syllabe.split('|')[0]
                        if hand == 'R':
                                syllabe = syllabe.split('|')[1]


                for key in syllabe:
                        if not_found:
                                rest=rest+key
                                continue
                        key_trans = key
                        
                        if not self.already_encoded and ( key in sounds.keys()):
                                key_trans = sounds[key]

#                        Log('key_trans', key_trans)
                        for key_trans_char in key_trans:
                                if key_trans_char in keys :
                                        keys = keys.split(key_trans_char)[1]
                                else:
                                        rest=rest+key
                                        not_found.append(key)
                                        key_trans=""
                                        break
                        if not not_found:
                                encoded = encoded + self.add_hyphen(key_trans)
                return (encoded,rest,not_found)

        def needs_hand(self, syllabe, already_encoded) :
                (encoded,rest,not_found) = self.get_hand_sound('L',syllabe,already_encoded)
                if not encoded :
                        return 'R'
                (encoded,rest,not_found) = self.get_hand_sound('R',syllabe,already_encoded)
                if not rest:
                        return 'L'
                return 'B'

                        
        def matching_syll(self, syllabe, keys) :
                for car in syllabe:
                        if car not in keys:
                                return False
                        keys = keys.replace(car,'')
                return True

        def encoded(self):
                piece = ""
                self.encoded_hand = ''
                if self.syllabe == "":
                        return piece
                if self.is_prefix:
                        # prefix always start left hand
                        self.hand = 'L'
                        self.already_encoded = True
                        self.init_keys_left()
#                if self.one_hand or self.syllabe.endswith('-'):

#                        self.encoded_hand = self.syllabe+'-'
                        Log('encoded one_hand', self.syllabe)
                        if self.one_hand :
                                return self.syllabe+'/'
                        if self.syllabe.endswith('-'):
#                                self.change_hand()
                                self.syllabe = self.syllabe[:-1]                    
#                                self.keys_left=''
#                        self.encoded_hand = self.encoded_hand + self.syllabe

#                        return self.syllabe
                
                if self.syllabe.startswith('-'):
                        self.syllabe = self.syllabe[1:]

                if self.syllabe.startswith('/'):
                        self.already_encoded = True
                        self.syllabe = self.syllabe[1:]          

            


                rest = self.syllabe
                count = 1

                cpt = (self.has_previous_R_and_L())
                if (self.previous is not None) :
                        if "PBLG" in self.previous.encoded_hand:
                                self.change_hand()
                                cpt = True
                        else:
                                self.keys_left = self.previous.keys_left
                                                                
                if self.is_suffix :
                        need_hand = self.needs_hand(self.syllabe, self.already_encoded)

                        if need_hand == 'B' and self.hand == 'R':
                                Log('need hand' , need_hand)
                                self.change_hand()
                                cpt= True
                        

                while rest and count<30:

                        if  self.is_left_hand() and cpt:
                                cpt = False
                                self.encoded_hand = self.encoded_hand+'/'
#                                piece = piece+'/'
                        (rest, not_found) = self.consume_syll(rest)

                        Log('piece',self.encoded_hand)

                        if rest :
                                self.change_hand()
                                cpt = True
                        count= count +1
                        Log('reste'+rest+":")
                        Log('encoded_hand', self.encoded_hand)
#                self.encoded_hand = self.add_hyphen(self.encoded_hand)
                return self.encoded_hand #piece

        def replace_hand(self, syllabe, items):
                for sound in items:
                        syllabe = syllabe.replace(sound[0], sound[1])
                return syllabe

class Steno_Encoding:
        DIPHTONGS = {
                # without i

                'sjasj§': 'SRAGS', #ciation
                '@v°n' : 'ENVH',
                'v°n' : 'VH',
                'vin' : 'VH',
                "jEn": "AEB",
                'Egze' : 'KP',
                'Egzi' : 'KPEU',
                'Eksi' : 'KPEU',
                'Eks' : 'KP',
                'ist' : '*EUS',
                'wan' : 'WOIB', #douane                
                'bRe': '-BS',
                "djO": "OD",
                "zj§": "GZ",
                'nal' : '-NL', 
                '@kR' : '-FRKS', #cancre
                "sj§": "GZ",
                'vul': 'WHR',
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                                'kE' : 'KE',
                'vERs' : '-/FRB', # divers
                'ERv' : '-/FRB', #v-erve
                'vEr' : '-/FRB', # cou-vert
                'vER' : '-/FRB', # travers
                'ijO' : 'AO',
                'jO' : 'RO|AO',

                'j@' : 'AEN' , # son ian
                '@l' : '-ANL', #enleve
                "RSi" : "VRPB",
                'REj' : '-RLZ' , #oreille

                "tER": "-TS",  #notaire
                "EtR" : "-TS" , #fenetre
                "RS" : "VRPB",# -rche
                "dZEk" : "PBLG",
                "dZ" : "PBLG",
                "bZEk" : "PBLG",
                "bZ" : "PBLG",
                "ps" : "S",
                'En' : 'AIB',
                "vaj" : "-FL",
                "vEj" : "-FL",
                '@v' : 'ENVH', #envenime

                't8' : 'TW', # fru-ctu-eux
#                "kR" : "KR", 
                "ks": "-BGS",
                '8a' : 'WA' , # ua in situation
#                "kR" : "RK",#can-cre
                 "kR" : "KR|RBG",#skrute
                'Ne'  : '-PGR',
                'on' : 'ON',
#                "di" : "D",
#                "mi" : "M",k§t
                'gRi' : 'TKPWR|GS',
                'gR' : 'TKPWR|GS',
#                "tR": "-TS", #tre
                "tR": "TR", #strate
                "8i": "AU",     # pluie
#                'ij': 'AO', # before jO
                'ij' : '-LZ', #ille
#                'jO' : 'AO',

                "j2": "AOEU",   # vieux
                "je": "AE",     # pied
                "jE": "AE",     # ciel
                "ja": "RA",     # cria
                "jo": "RO",     # bio

#                "jO": "ROE",    # fjord # TODO unsure
#                "jo": "AO",     # bio # TODO Some conflict there. "-R can be read as i" (above), but the diphtongs are more important I guess?
#                "jO": "RO",     # fjord
                "j§": "AO",     # av_ion_
                "kw": "KW",
                'k§' : 'KOEPB-', # content
#                "wE": "WAEU",
                "wE" : "WE",
                "§t" : "OFRPT",
                "@S" : "-AFRPBLG",
                "5S" : "-EUFRPBLG",
                '@p' : '-AFRP' , #campe
                '§p' : '-OFRP', # trompe
                'pl' : 'PL',
                "ER" : "AIR",
                'gl' : 'GL|-FRLG', #glace or angle
                "wa": "OEU",    # froid
                "w5": "OEUPB",  # loin
                "wi": "AOU",    # oui
                "j5": "AEPB",   # chien
                "ey": "EU",     # r_éu_nion
#                "vR": "VR",
                'oo' : 'O',    #zoo
                "ya": "WA",     # suave
#                "ij": "LZ",    # bille # TODO Maybe not a diphtong, but a word ending/consonant thing

                'fl': "FL",
                "5" : "IN",
                'u' : 'OU',
                '1' : 'U',
#                'e' : '',
                "@": "AN",     # pluie
                "E" : "AEU", #collecte
#                "e" : "AEU", #collecte
                'N' : 'PG',
                'd' : 'D',
                "y": "U",       # cru

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
                "o": "OE",      # haut
                "O": "O",       # mort

#                "y" : "",
                "u": "OU",      # mou
                "5": "EUFR",    # vin
                "8": "U",       # huit
                "§": "ON",
                # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

        }

        def __init__(self, syllabes, prefix, suffix):
                self.syllabes = syllabes
                self.prefix = prefix
                self.suffix = suffix
                Log('steno_suffixes' , vars(self))

        def diphtongs_try(self, word):
                new_word=word
                final_word = ''
                items = self.DIPHTONGS
                keys = self.DIPHTONGS.keys()
#                self.found_sound = ''
                nb_char = len(word)
                while new_word != '' :
                        Log(nb_char,word[:nb_char])
                        if items.get(word[:nb_char]) is not None:
#                                self.found_sound=diphtong[1]
                                final_word = final_word + "+"+items[word[:nb_char]]+"+"
                                break
                        nb_char = nb_char-1
                        if new_word :
                                new_word = new_word[nb_char:]
                                                        

                return final_word

        def find_matching(self, syll, word) :
                Log('find match word', word)
                for diphtong in self.DIPHTONGS.items():
                        key = diphtong[0]
                        if key in word:
                                Log('find key', key)
#                                self.found_sound = diphtong[1]
                                if word.startswith(key):
                                        syll[key] = diphtong[1]
                                        end = word.replace(key, '')
                                        if end :
                                                for  findsyll in self.find_matching(syll,end).items():
                                                        syll[findsyll[0]] = findsyll[1]
                                        return syll
                                if word.endswith(key):
                                        start = word.replace(key, '')
                                        if start :
                                                for  findsyll in self.find_matching(syll,start).items():
                                                        syll[findsyll[0]] = findsyll[1]
                                        syll[key] = diphtong[1]
                                        return syll
                                splitted = word.split(key)
                                start  =splitted[0]
                                for  findsyll in self.find_matching(syll,start).items():
                                        syll[findsyll[0]] = findsyll[1]
                                syll[key] = diphtong[1]
                                
                                end = splitted[1]
                                for  findsyll in self.find_matching(syll,end).items():
                                        syll[findsyll[0]] = findsyll[1]
                                return syll
                syll[word] = ""
                return syll
                                
                                
        def diphtongs(self, word):
                before = ''
                after = ''
                new_word=word
                syll_dict = {}
                final_word = word
                items = self.DIPHTONGS
                keys = self.DIPHTONGS.keys()
#                self.found_sound = ''
                nb_char = len(word)
                for diphtong in self.DIPHTONGS.items():
                        
                        if diphtong[0] in new_word :
                                final_word = final_word.replace(diphtong[0], "+"+diphtong[1]+"+")
                                Log('final_word',final_word)

                                new_word = new_word.replace(diphtong[1],'')
                                Log('new_word',new_word)
#                        self.found_sound=diphtong[1]

    
                
        def encode(self):
                self.word_encoded = ""
                previous = None
                count_syll = 1
                one_hand=False
                next_syll = self.syllabes
                if self.prefix:
                        if '/' in self.prefix:
                                one_hand = True
                                self.prefix = self.prefix.replace('/','')
                        previous = Syllabe(self.prefix, None, self.prefix).prefix()
                        if (one_hand):
                                previous.set_one_hand()
                        self.word_encoded = previous.encoded()
                        Log('prefix encoded', self.word_encoded)
                        if (one_hand):
                                self.hand='L'
                        count_syll = 2
                
                for piece in self.syllabes:
                        if piece == "":
                                continue
                        Log('piece',piece)
                        sylls = {}
                        sylls = self.find_matching(sylls, piece)
                        Log('sylls' , sylls)


#                        piece = self.diphtongs(piece)
                        Log('word encoded' , self.word_encoded)
#                        Log('found sound dif' , self.found_sound)

                        Log('dif',piece)
#                        piece = self.voyels(piece)
                        Log('voyel',piece)
                        
                        if piece == "":
                                continue
                        for mysyll in sylls.items() :
                                new_piece = mysyll[0]
                                if mysyll[1] != "":
                                        new_piece = mysyll[1]
                                else:
                                        new_piece = self.voyels(new_piece)
                                        new_piece = new_piece.upper()
#                        for new_piece in piece.split('+'):
                                Log('syllabe',new_piece)
                                syllabe = Syllabe(new_piece.upper(), previous,next_syll)
                                encoded = syllabe.encoded()

                                Log('encoded syllabe', encoded)
#                                if self.found_sound and self.found_sound.endswith("RK") and self.word_encoded.endswith('PB'):

#                                        Log('found sound', self.found_sound)
#                                        self.word_encoded = self.word_encoded[:2]
#                                        encoded = 'KS'
#b                                         or self.found_sound.endswith("BGS")) 
                                
                                self.word_encoded = self.word_encoded+ encoded
                                
                                Log('encoded word', self.word_encoded)
                                previous = syllabe
                        next_syll = self.syllabes[count_syll:]
                        count_syll = count_syll+1
                Log('WORD ENCODED BEFORE SUFFIX', self.word_encoded)
                if self.suffix :
                        syllabe = Syllabe(self.suffix,previous, next_syll).suffix()
                        self.word_encoded = self.word_encoded + syllabe.encoded()
                if self.word_encoded.startswith('/'):
                        self.word_encoded = self.word_encoded[1:]
                Log('WORD ENCODED ', self.word_encoded)
                return  self.word_encoded.replace('//','/')

        def voyels(self, word):
                new_word=word
                for char in word:
                        if char in self.VOWELS:
                                new_word = new_word.replace(char, self.VOWELS[char])
                return new_word

