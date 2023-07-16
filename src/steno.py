import sys
import copy
import re

from src.word import Word

from src.cutword import Cutword
from src.syllabe import Syllabe
from src.log import Log
from src.steno_encoding import Steno_Encoding
class Ortho:

        sounds = ''
        sound = ''
        replace_by = ''
        steno_str =''
        prefix = False
        check_alternative = False
        alternative_str = ''
        one_hand = False
        mandatory=False
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

        def set_mandatory(self) :
                self.mandatory = True
                return self

        def get_alternative_str(self, word, suffix_str) :
                return word.replace(suffix_str, self.alternative_str)


class OrthoSuffix(Ortho):
        
        def convert(self,phonetic,syll) :
                for sound in self.sounds:
                        if syll.endswith(sound) :
                                syll = syll[:-len(sound)]
                                self.steno_str = self.replace_by
                                Log('ortho suffix convert',syll)
                                return syll
                return False

        def can_be_converted(self, syll):
                for sound in self.sounds:
                        if syll.endswith(sound) :
                                self.sound = sound
                                return True
                                
                return False

class OrthoPrefix(Ortho):
        def convert(self,phonetic, syll):
                for sound in self.sounds:

                        if syll.startswith(sound) :
                                syll = syll[len(sound):]
                                self.steno_str = self.replace_by
                                Log('Ortho prefix convert:',syll)
                                return syll
                return False

        def can_be_converted(self, syll):
                for sound in self.sounds:
                        if syll.startswith(sound) :
                                self.sound = sound
                                return True
                return False
class Steno:
        PREFIXES = {
                # all already encoded
#                "s2": "S", # ce mais pas ceux
                "d°m@d" : "TK-PLD",
                "sypER" : "SP-R/",
                "sufR" : "STPR",
                'k§f':'KW',
                'Oto' : "AOT",
                "tEknO" : "T",
                "aREt" : "ART",
                "apO" : "PAO",
                "aplo" : "PHRAO",
                "aplO" : "PHRAO", 
                "tR@s" : "TRAPBS/",
                "tR@z" : "TRAPBS/",
                "tEl" : "THR-",
                'Egzek' : 'KP',
                'Egze' : 'KP',
                'Egzi' : 'KPEU',
                'Eksi' : 'KPEU',
                'pER' : 'PR',

                'Eks' : "KP|-/BGS",
                'ade' : 'AD', # sound
                'm°n' : "KH",#men
                'min' : "KH",#min
                'm2n' : 'KH', #men
                't°n' : 'TH', #tenace
                'ten' : 'TH', #tenace

                'ina' : 'TPHA',
                "syp" : "SP",
                'inE' : 'TPHAEU',
                'ini' : 'TPHEU',
                'in§' : 'TPHOPB',
                'ino' : 'TPHO',
                'iny' : 'TPHU',
                '5sy' : 'STPHU',
                '5si' : 'STPHEU',
                '5sa' : 'STPHA',
                '5se' : 'STPHE',
                "s@t" : "ST",
                "tE": "TAEU",  #terminer
                '5k' : '/EUFRPB',
                "kR" : "KR", #craquait
                "S°" : "SK",
                "@t" :"SPW",
                "5t" :"SPW",
                "R°" : "R",
#                "Z°" : "SKW-", #gelé
#                "gl" : "
                "Sa" : "SK",
                'ke' : 'K',
                'dR' : 'TKR',
                'sin' : 'STPH',
                'sp' : 'SP',
                'sn' : 'STPH',
#                'k§' : '-KON', # conte
                'k§' : 'KOPB/', # content
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
                'z' : 'SWR',
                'a':'A|AE/',
                'e':'E'
        }

        ORTHO_PREFIXES = {
                'multi' :OrthoPrefix('mylti', 'PHULT'),

                'égal' : OrthoPrefix('egal', 'AELG'),

                'corr' : OrthoPrefix('kOR', 'KR'),
                'coll' : OrthoPrefix('kOl', 'KHR'),
                "comm" : OrthoPrefix('kom|kOm','KPH'),
#                "cont" : OrthoPrefix('k§t','KOEPB/T|KOPB/T|ST'),
                "com" : OrthoPrefix('k§','K*/|K'),
                "con" : OrthoPrefix('k§','KOEPB/|KOPB|S'),
                'inter' : OrthoPrefix('5tER', 'EUPBTS'), #SPWR
                'ind' : OrthoPrefix('5d', 'SPW'),
                'end' : OrthoPrefix('@d', 'SPW'),
                'réu' : OrthoPrefix('Rey', 'REU'),
                'fin'  : OrthoPrefix('fin', 'WH'),
                'fen'  :OrthoPrefix('f°n', 'WH'),
                'y'  :OrthoPrefix('j', 'KWR'),
                
#                "a" : OrthoPrefix('a-','AE-'), # sound

                }

        
        ORTHO_SUFFIXES = {
                'babilité' : OrthoSuffix('babilite','-/BLT'),
                'cation' : OrthoSuffix('kasj§','-/BGS'),

                'lation' : OrthoSuffix('lasj§', '-/LGS'),

                'bilité' : OrthoSuffix('bilite','-/BLT'),
                'ilité' : OrthoSuffix('ilite','ILT|LT'),
                'lité' : OrthoSuffix('lite','-/LT'),
                'bilise' : OrthoSuffix('biliz','-/BLZ'),
                'ralise' : OrthoSuffix('Raliz','/RALZ'),
                'lise' : OrthoSuffix('liz','-/LZ'),

                'rité' : OrthoSuffix('Rite', '-/RT'), # securite
                'bité' : OrthoSuffix('bite','-/BT'),
                'tivité': OrthoSuffix('tivite', '/TEUFT'),
                'vité': OrthoSuffix('vite', '-/FT'),
                'cité': OrthoSuffix('site', '-/FT'),
                'sité': OrthoSuffix('site', '/ST*E'),
                'igé': OrthoSuffix('iZe', 'EG'),
                'iger': OrthoSuffix('iZe', '*EG'),
                'ience' : OrthoSuffix('j@s', 'AENS'),
#                'ance' : OrthoSuffix('@s', '-NS'),
#                'ence' : OrthoSuffix('@s', '-NS'),
                'ande' : OrthoSuffix('@d', '-/PBD'),
                'aux' : OrthoSuffix('o', 'O*EX'),
                'ité' : OrthoSuffix('ite','ITD|T'),
                'gueur' : OrthoSuffix('g9R' , '-RG'),
                'deur' : OrthoSuffix('d9R' , '-RD'),
                'lheur' : OrthoSuffix('l9R' , '-RL'),
                'leur' : OrthoSuffix('l9R' , '-RL'),
                "cteur" : OrthoSuffix("kt9R", "-RT") ,
                "teur" : OrthoSuffix("t9R", "-/RT") ,

                "nheur" : OrthoSuffix("n9R", "-RN") ,
                "neur" : OrthoSuffix("n9R", "-RN") ,
                "rtion" : OrthoSuffix("Rsj§", "-RGS"),
                "ration" : OrthoSuffix("Rasj§", "-RGS"),
                "ctrice" : OrthoSuffix("ktRis", "-/RTS") ,
                "trice" : OrthoSuffix("tRis", "-/RTS") ,
                'cienne' : OrthoSuffix('sjEn', '-/GZ'),
                "telle" : OrthoSuffix("tEl" , "-/LGTS"),
                "tel" : OrthoSuffix("tEl" , "-/LGTS"),
                "velle" : OrthoSuffix("vEl", "-/FL"),
                "quelle" : OrthoSuffix("kEl", "-/BLG"),
                "quel" : OrthoSuffix("kEl", "-/BLG"),

                "ière"  : OrthoSuffix('jER', 'A*ER').set_mandatory(),
#                "ier"  : OrthoSuffix('jER|ije|je', '/AER').set_mandatory(),

                "iée"  : OrthoSuffix('je', '/AED').set_mandatory(),
                "ié"  : OrthoSuffix('je', 'AE').set_mandatory(),

                "iel"  : OrthoSuffix('jEl', 'AEL'),
                'ive' : OrthoSuffix('iv|ive|iv', '/*EUF'),
                'if' : OrthoSuffix('if', '/*EUFL'),
                'cien' : OrthoSuffix('sj5', '-GS'),
                "ain" : OrthoSuffix("5", "IN"),
                'cte' : OrthoSuffix('kt', 'KT'),
                "ène" : OrthoSuffix("En","/*EB"),
#                "eur" : OrthoSuffix("9R","-AO*R"),

                "uelle" : OrthoSuffix("yEl|8El","/*UL|/W*EL").set_mandatory(),
                "uel" : OrthoSuffix("yEl|8El","/UL|/WEL"),
                "anche" : OrthoSuffix("@S","/AFRPBLG"),
                "rche" : OrthoSuffix("RS","-/FRPB"),
                "che" : OrthoSuffix("S","-/FP"),
                "chage" : OrthoSuffix("SaZ","-/FPG"),
                "oué" : OrthoSuffix("we|wE","/W*E"),
                "way" : OrthoSuffix("we|wE","/W*E"),
                "ué" : OrthoSuffix("8e","/W*E"),
                "cise" :OrthoSuffix("siz", "-/RBZ"),
                "cis" :OrthoSuffix("si", "-/RB"),

                "ssis" :OrthoSuffix("si", "-/RB"),
                "ci" : OrthoSuffix("si", "-/RB"),
                "cet" : OrthoSuffix("sE", "SZAEU"),
                "ce" : OrthoSuffix("s", "-SZ").alternative('ss'),
                "elle" : OrthoSuffix("El", "/*EL").set_mandatory(),
                "el" : OrthoSuffix("El", "/EL"),
                
                "th" : OrthoSuffix("t", "-GT"),
                "the" : OrthoSuffix("t", "-GT"),
                "a" : OrthoSuffix("a", "-Z|/*Z"),
                

        }
                

        REAL_SUFFIXES = {
                "En" : "A*IB",
                
                "wE": "-/W*E",


        }

        # if start with / then dont convert
        # - for right hand
        # | for multiple choices
        SUFFIXES = {
                'm@tER' : '/PHAPBTS|-/PLTS',
                'zERvasj§': '/FRBGS', #rvation
                "pRasj§":"/RPGS",
                '@tER' : '-/PBTS|/APBTS',
                'sjasj§': '/SRAGS', #ciation
                'pasj§' :  '-PGS', # preocuppation
                't82' : '/TWAO*', # fru-ctu-eux
                'sjasj§': '/SRAGS', #ciation
                '@sjOn' : "ANGZ", #mentionne
                '5ksj§' : "-/PBGS", #distinction
                '§ksjOn' : "/OPBGS/*B", #fo-nctionne
                "mEtR": "-/PLTS",
                'st@s': '/STAPBS',
                'ij@d' : 'IND',
                'ksj§' : "/*BGS", #friction
                "zj§": "-/GZ",
                "vwaR" : "-/FRS",
                "val" : "-/FL",
                "vaj" : "-/FL",
                "vEl" : "-/FL",
                'Rnal' :'-RBL',
                'sjOn' :'-/GZ',
                't8ER' : 'TW*R', # portuaire
                'ktyR' : '-TS', #ture
                'tyR' : '-TS', #ture
                '@gl' : '/AFRLG',
                '§gl' : '/OFRLG',
                '5gl' : '/EUFRLG',
                'm°n' : "/KH",#men
                'diR' : '-/DZ',
                "win": "AOUB",    # oui
                'nal' : '-/PBL', #canal
                'mas' : 'MS', #amasse


#second option                'sjOn' :'-/GS/*B',
                "tER": "-TS",  #notaire
#                "EtR" : "-TS" , #fenetre
                "jEm" : "/A*EPL",
#                "jER" : "AER" , #caissiERE
                "jasm" : "/KWRAFPL",
                "jEn": "AEB",
                "sj§" : "GS",
                "lOZik" : "LOIK",
                "lOZist" : "/HRO*EUS",
                "lOZi" : "LO*IG",
                "lOg" : "LO*EG",
                "p9R" : "-/RP",
                "pORt" : "-/RPT",
                "poR" : "-/RP",
                "pOR" : "-/RP",
                "int" : "/EUPBT",

                "pid" : "-PD",
#                "fis" : "-WEUS",
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                "kEl" : "-/BLG",
                "§kl" : "/OFRBLG", # oncle
                "akl" : "/AFRBLG", 
#                "je" : "AER" , #caissIER

#                "l9R" : "-RL",
#                "d9R" : "RD",
                "dabl" : "/TKABL",
                "v°m@" : "-/FPLT",
                "@sj§": "/APBS",    # p_ension_
                "jast" : "YA*S|/KWRAFT|/RAFT",
                "vwaR" : "-/FRS",

                "Ribl" : "-/RBL",
                "@tR" : "-/PBTS", #-ntre
                "stR" : "-/TS", #-stre
                "RtR" : "-/RTS", #-rtre
                "§pR" : '/OFRPS',
                "@bl": "/AFRBL",   # tremble
                "§bl": "/OFRBL",  # comble
                "1bl": "/UFRBL",  # comble
                "@bR": "/AFRBS",   # ambre
                "5bR": "/EUFRBS",  # timbre
                "§bR": "/OFRBS",   # ombre
                "5b": "/EUFRB",  # limbe
                "§b": "/OFRB",  # comble
                "ks": "-/BGS",
                'st' : '-/FT',#new rule
#                "st" : "-*S",
                "t@" : "TAN", #content
                "ve": "/WE", # releve
                "iN§" : "/HO*PB", #bourguignon
                "N§" : "/HO*PB", #bourguignon
                "@Z" :"/APBLG", # ange
                "5Z" :"/EUPBLG", # linge
                "§t" : "/OFRPT", # prompte
                "5p" : "/EUFRP",
                '@pl' : "/AFRPL",
                "9R":"/AO*R",
                'oo' : 'O',    #zoo
                "je": "AE",     # pied
                '@p' : '/AFRP' , #campe
                'ilm' : 'LIM' , #film -> flim
                'ylb' : 'LUB' , #bulbe -> blub
                'alv' : 'LAV' , #valve -> vlav
                'gl' : 'LG' , #sigle -> silge
                '§p' : '/OFRP', # trompe
                'Ribl' : '-/RBL',
                'Rbal' : '-/RBL' , #verbal
                '5bal' : '/EUFRB', # trimb          
                'bal' : '-/RB' , #global
                "Ral" : "RAL|-/RL",
                'kE' : 'KE',
                'vERs' : '-/FRBS', # diverses
                'vERn' : '-/FRB', # gouverne
                'ERv' : '-/FRB', #v-erve
                'vEr' : '-/FRB', # cou-vert
                'vER' : '-/FRB', # travers
                'REj' : '-/RLZ' , #reille
                
#                'fER' : '-/FRB', #o-ffert
                'fER' : '-/FR', #faire sphere
                'vR' : '-/FR', # iv-re
                'fR' : '-/FR' , #sou-fre
                '@l' : 'ANL', #branle
                'zm' : '-/FPL',
                'sm' : '-/FPL',
                'di' : '/*D',  #interdit ?
                "tEkt" :  "/T*BG",
#                "EtR" : "-/TS",
                "SEt" : "-/FPT" , # achete
#                "RZ" : "-/RPBLG",
                "RZ" : "RG",
                "bl" : "-/BL",
                "@S°" : "AFRPBLG",
                "fR" : "-/FR", #souffre
                "fl" : "-/FL", #souffle
                'sk°'  : '-/FBG', #puisque
                'sk' : '-/FBG',


                "Re":"/R*E|RE",
                'z§':'-/GZ',
                "@S" : "/AFRPBLG",
                "@s" : "/APBS|-/PBS",

                "ZE" : "G",

                'ij' : '-/EULZ|-/LZ', #ille

                "t°m@" : "-/PLT",
                "m@" : "-/PLT",
                "En" : "AIB",
                "ER" : "AIR",
                "@d" :"-/PBD",

                "dR" : "-/DZ" ,# ajoin-dre
                "@b": "/AFRB",   # jambe
                "tR": "-/TS", #tre - 
                "bR":"-/BS",  #-bre
                "pR":"-/PS", #-pre
                "nEs" : "/BS",
                "Et" : "/AEUT",
                "mn" : "/KH",
#                'El' :'-/FL',
                "E" : "/AEU",
                "e" : "-/D",
                "n" : "-/B",
                'j' : '-/LZ',
                "§" : "OPB|/*PB",
#                "sm" : "-/FP",
                'o' : 'OE',
                'a' : '-Z|/*Z',
                'O' : 'O',
#                't' : 'T',
                'N' : 'PG',

                "Z" : "G", # rage
                'u' : 'OU',
#                "S" : "-/FRPBLG",
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
        needs_star = False
        prefix = ""
        steno_word = ""
        syllabes = []
        ending = ""
        start = ""
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

        def ortho_starting_with_des(self,myword, phonetics):
                word = myword
                cutword=Cutword(phonetics)
                syll = phonetics
                Log('Starting with des? ', syll)
#                if not syll.startswith('dez') and not syll.startswith('des') and not syll.startswith('d°s'):
                if not word.word.startswith('de') and not word.word.startswith('dé'):
                        return cutword
                next_letter = word.word[:4].upper()
                Log('> 3rd letter:', next_letter)
                if word.word.startswith('dés') and next_letter[-1] in ['A','E','É','I','O','U', 'Y'] :
                        self.prefix = {'TKAOEZ|STK' : 'dez'}
                        remains = phonetics[3:]
                        replace ='dez' 
                        by='TKAOEZ|STK'

                        return self.create_cutword(phonetics,remains,replace,by)


                if word.word.startswith('dé')  or word.word.startswith('des') or ((next_letter.endswith('O') or next_letter.endswith('E') or next_letter.endswith('I') or next_letter.endswith('A') or next_letter.endswith('U') or next_letter.endswith('@') or next_letter.endswith('Y'))) :
                        remains=phonetics
                        replace ='de' 
                        by='STK'
                        self.prefix = {'STK' : 'de'}
                        remains = phonetics[2:]
                        if phonetics.startswith('dez'):
                                self.prefix = {'STK':'dez'}
                                replace ='dez' 
                                by='STK'
                                remains = phonetics[3:]
                        if phonetics.startswith('dek'):
                                self.prefix = {'STK':'dez'}
                                replace ='dez' 
                                by='STK'
                                remains = phonetics[3:]

                        if phonetics.startswith('des'):
                                self.prefix = {'STK':'des'}
                                replace ='des' 
                                by='STK'
                                remains = phonetics[3:]

                        if phonetics.startswith('d°s'):
                                replace ='d°s' 
                                by='STK'
                                self.prefix = {'STK':'d°s'}
                                remains = phonetics[3:]

                        if (phonetics.startswith('def')):
                                replace ='def' 
                                by='STKW'
                                self.prefix = {'STKW' : 'def'}
                                remains = phonetics[3:]

                        Log('> syll: ', remains)
                        return self.create_cutword(phonetics,remains,replace,by)

                return cutword


                
        def ortho_add_aloneR_infinitif_firstgroup(self, word, phonetics):
                cutword=Cutword(phonetics)
                if word.word.endswith('ier'):
                        self.ending = "AER"
                        self.ending_syll = phonetics[:-2]
                        Log('Fini par ier')
                        if phonetics.endswith('jER') or phonetics.endswith('ije'):
                                self.ending_syll = phonetics[:-3]
                        Log('Fini par ier'+self.ending_syll)
                        cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True

                        return cutword
                verb_word = self.find_same_word_verb(word)
                if verb_word.is_verb() and verb_word.is_infinitif()  and verb_word.word.endswith('er'):
                        if verb_word.word.endswith('iger'):
                                self.ending = "*EG"
                                self.ending_syll = phonetics[:-3]
                                cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword
                        self.ending = "-R"
                        self.ending_syll = phonetics
                        if verb_word.syll.endswith('e') :
                                self.ending_syll = phonetics[:-1]
                        cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True

                return cutword

        def ortho_add_alone_keys_on_noun(self,word, phonetics):
                cutword=Cutword(phonetics)
                if word.is_verb():
                        return cutword
                


                if word.word.endswith('ée') and not word.word.endswith('iée'):
                        self.ending_syll = phonetics[:-1]
                        self.ending = "ED"
                        
                        cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending)
                        cutword.mandatory=True
                        return cutword

                                
                if word.word.endswith('ette'):
                        self.ending = "/*T"
                        if word.syll.endswith('Et') :
                                Log('Fini par et')
                                self.ending_syll = phonetics[:-2]
                        return self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending)
                if word.is_plural() and word.word.endswith('s'):
                        self.ending = "-S"
                        return self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending)

                return cutword



        def check_prefixes(self,word, syll):
                Log('check prefixes start')
                mylist =[]
                cutword=Cutword(syll)
#                mylist.extend( cutword.generate())
                cutword = self.prefixes(syll,word)
                
                if cutword.has_found():
                        mylist.extend( cutword.generate())
                if cutword.mandatory==True:
                        Log('mandatory',cutword.steno)
                        return mylist
                cutword= self.ortho_starting_with_des(word, syll)

                if cutword.has_found():
                        mylist.extend(cutword.generate())
                for orth in self.ORTHO_PREFIXES.items():
                        if word.word.startswith(orth[0]):
                                Log(vars(orth[1]))
                                ortho = orth[1]
                                ortho.prefix = True

                                if (ortho.can_be_converted(syll)):
                                        syll = ortho.convert(word,syll)
                                        cutword.set_remains(syll)
                                        cutword.set_ortho_rule()
                                        cutword.set_replaced_by(ortho.sound, ortho.steno())
                                        self.prefix = {ortho.steno() : ortho.sound}
                                        Log('prefix test' , self.prefix)
                                        mylist.extend(cutword.generate())
                                        return mylist
                mylist.extend(cutword.generate())
                return mylist

        def create_cutword(self,phonetics,remains,replace,by, ortho =False, separate_stroke=False):
                cutword=Cutword(phonetics)
                cutword.set_replaced_by(replace, by)
                cutword.set_remains(remains)
                if ortho:
                        cutword.set_ortho_rule()
                if separate_stroke:
                        cutword.set_separate_stroke()
                return cutword
                
        
        def ortho_add_alone_keys_on_verb(self,word, phonetics):
                verb_word = self.find_same_word_verb(word)
                Log(vars(verb_word))
                cutword=Cutword(phonetics)

                if not verb_word.is_verb():
                        Log('word is not a verb')
                        return cutword
                if verb_word.has_noinfoverb():
                        return cutword

                Log('Verbe')
                
#                if (not self.ending_syll):

                self.ending_syll = phonetics
                Log('ending syll',phonetics)
                if  verb_word.is_passe_compose():
                        if verb_word.syll.endswith('8e') or verb_word.syll.endswith('wE') or verb_word.syll.endswith('we') :
                                self.ending = "/W*E"
                                self.ending_syll = phonetics[:-2]
                                cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword
                        if verb_word.syll.endswith('je') :
                                self.ending = "/AE"
                                self.ending_syll = phonetics[:-2]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword
                        
                        if verb_word.syll.endswith('e') :
                                self.ending = "/-D"
                                self.ending_syll = phonetics[:-1]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword


                if verb_word.is_conditionnel():
                        self.ending = "/-RS"
                        if verb_word.is_third_person_plural():
                                self.ending = "RAEUPBT"
#                                self.ending = "/-RPB"
                                self.ending_syll = phonetics[:-2]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword

#                                                        if verb_word.word.endswith('rait'):
#                                        self.ending = "-RTS"

                        if ( verb_word.word.endswith('rait')) and verb_word.syll.endswith('E') :
                                self.ending = "/-RS"

                                self.ending_syll = phonetics[:-2]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword

                        if verb_word.syll.endswith('RE') :
                                self.ending_syll = phonetics[:-2]


                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword


                if verb_word.is_vous_ind_present():
                        self.ending = "/*EZ"

                        if verb_word.syll.endswith('Re') :
                                Log('indic')
                                self.ending = "/R*EZ"
                                self.ending_syll = phonetics[:-2]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword

                        if verb_word.syll.endswith('e') :
                                self.ending_syll = phonetics[:-1]
                                cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword

                if verb_word.is_participe_present():
                        Log('participe present')
                        self.ending = "-G"
                        if verb_word.syll.endswith('j@')  :
                                self.ending_syll = phonetics[:-2]
                                cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending, True, True)
                                cutword.mandatory=True
                                return cutword
                        if verb_word.syll.endswith('@') :
                                self.ending_syll = phonetics[:-1]
                                cutword=self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending, True, True)
                                cutword.mandatory=True
                                return cutword


                if verb_word.ending_with('a'):
                        self.ending = "/*Z"
                        self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword
                if verb_word.ending_with('erons'):
                        self.ending = "ROPB"
                        self.ending_syll = phonetics[:-3]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword
                if verb_word.ending_with('ont'):
                        self.ending = "OPBT"
                        self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword
                if verb_word.ending_with('ons'):
                        self.ending = "OPB"
                        self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword


                if verb_word.ending_with('ais'):
#                if verb_word.is_imparfait():
                        Log('imparfait')
                        self.ending = "/AEUS"
#                        self.ending = "/AEUS"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True,True)
                        cutword.mandatory=True
                        return cutword

                if verb_word.ending_with('ai'):
#                if verb_word.is_imparfait():
                        Log('futur')
                        self.ending = "/AEU"
#                        self.ending = "/AEUS"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True,True)
                        cutword.mandatory=True
                        return cutword

                if verb_word.ending_with('ait'):
#                        if verb_word.is_third_person_singular():
#                                self.ending = "/AEUT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = phonetics[:-1]
                        self.ending = "/-S"
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending, True)
                        cutword.mandatory=True
                        return cutword

                if verb_word.ending_with('it'):
#                if verb_word.is_imparfait():
                        self.ending = "/EUT"
#                        self.ending = "/AEUS"
                        if verb_word.syll.endswith('i') :
                                self.ending_syll = phonetics[:-1]
                        cutword= self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True,True)
                        cutword.mandatory=True
                        return cutword

                if verb_word.ending_with('aient'):
#                        if verb_word.is_third_person_plural():
#                                self.ending = "AEUPBT"
                        self.ending = "/AEUPBT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = phonetics[:-1]
                                cutword = self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                                cutword.mandatory=True
                                return cutword


                if verb_word.ending_with('ent'):
#                        if verb_word.is_third_person_singular():
#                                self.ending = "/AEUT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = phonetics[:-1]
                        self.ending = "/-PBT"
                        cutword = self.create_cutword(phonetics,self.ending_syll,self.ending_syll,self.ending,True)
                        cutword.mandatory=True
                        return cutword


                # if verb_word.syll.endswith('E') :
                #         self.ending_syll = verb_word.syll[:-1]

                if not self.ending  :
                        Log('not found ending',verb_word)
                return cutword

                
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


        def prefixes(self, phoneme, word_class):
                cutword = Cutword(phoneme)
                if word_class.word.startswith('h') :
                        self.prefix = {'H' : ''}
                        cutword.set_remains(phoneme)
                        cutword.set_replaced_by('','H')
                        cutword.mandatory=True
                        return cutword
                if (word_class.word.startswith('y') and phoneme.startswith('j')):
                        self.prefix ={'KWR' : 'j'}
                        new_word = phoneme.replace('j','',1)
                        cutword.set_remains(phoneme.replace('j','',1))
                        cutword.set_replaced_by('j','KWR')
                        return cutword
                

                if  self.pronoun:
                        self.prefix={'Y': 'y'}
                        cutword.set_remains(phoneme)
                        cutword.set_replaced_by('y','Y')
                        return cutword
                for prefix in  self.PREFIXES.items():
                        if len(re.split("^"+prefix[0], phoneme))>1:
                                cutword.set_remains(re.split("^"+prefix[0], phoneme)[1])
                                cutword.set_replaced_by( prefix[0], prefix[1])
                                Log('found prefix : ',prefix[0])
                                self.prefix = {prefix[1] : prefix[0]}
                                return cutword

                return cutword


        def suffixes(self, phoneme, TAB):
                cutword = Cutword(phoneme)
                for suffix in TAB.items():
                        if len(re.split(suffix[0]+"$", phoneme))>1:
                                cutword.set_remains(re.split(suffix[0]+"$", phoneme)[0])
                                cutword.set_replaced_by(suffix[0],suffix[1])
                                self.suffix = suffix[1]
                                return cutword
#                                return re.split(suffix[0]+"$", new_word)[0]

                
                return cutword

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

        
        def transform(self,word):
                                


                self.final_encoded = []
                myword = self.find(word)
                if not myword:
                        return ""
                Log(vars(myword))
#                myword.syll = self.try_to_remove_woyel(myword)
#                self.prefix ={}
#                self.suffix =""
                self.final_encoded=self.newtransform(myword)
                Log('Final words encoded: ' , self.final_encoded)
#                self.final_encoded=self.basic_transform_by_syllabes(myword)
                Log('The word is a verb ? ' , myword.is_verb())
                has_homophone = self.has_homophone(myword)
                Log('Has homophone ? ' , has_homophone)
                finals = self.final_encoded
                Log('Final words encoded: ' , self.final_encoded)
                return self.final_encoded

        def check_ending(self, word,prefix) :
                phoneme  = prefix.get_remains()
                cutword = Cutword(phoneme)
                mylist  =[]

                Log("phoneme",phoneme)
                onverb = self.ortho_add_alone_keys_on_verb(word,phoneme)
                Log("on verb",vars(onverb))
                                        
                if onverb.has_found():
                        return  onverb
                infinitif = self.ortho_add_aloneR_infinitif_firstgroup(word, phoneme)
                if infinitif.has_found():
                        return infinitif
                infinitif = self.ortho_add_alone_keys_on_noun(word, phoneme)
                if infinitif.has_found():
                        return infinitif
                return False

        def check_suffixes(self, word, prefix) :
                phoneme  = prefix.get_remains()
                cutword = Cutword(phoneme)
                mylist  =[]
                Log("phoneme",phoneme)
                mandatory=False
                for orth in self.ORTHO_SUFFIXES.items():

                        if word.word.endswith(orth[0]) :
                                ortho = orth[1]
                                if ortho.check_alternative :
                                        if  self.find_spelled_word(ortho.get_alternative_str(word.word,orth[0])):
                                                Log('continue check alternative')
                                                continue
                                Log(vars(ortho))
                                Log('ORTHO SUFFIXE can be ' , ortho.can_be_converted(phoneme))
                                if (ortho.can_be_converted(phoneme)):
                                        syll = ortho.convert(word,phoneme)
                                        cutword.mandatory=ortho.mandatory
                                        mandatory=ortho.mandatory
                                        cutword.set_remains(syll)
                                        cutword.set_ortho_rule()
                                        cutword.set_replaced_by(orth[0],ortho.steno())
                                        Log('converted ok, remains:',syll)
                                        mylist.extend(cutword.generate())
                Log('ORTHO SUFFIXE mandatory ' ,mandatory)
                if (mandatory):
                        return mylist
                cutword = self.suffixes(phoneme,  self.SUFFIXES)
                if (cutword.has_found()) :
                        Log('found cutwor:',vars(cutword))
                        mylist.extend(cutword.generate())
                        return mylist


                cutword = self.suffixes(phoneme,  self.REAL_SUFFIXES)
                if (cutword.has_found()) :
                        mylist.extend(cutword.generate())
                        return mylist
                Log('found cutwo 2:',vars(cutword))
                mylist.extend(cutword.generate())
                return mylist

        def prefix_h(self, word, syll) :
              
                if word.startswith('h') :
                        self.prefix = {'H' : ''}
                #and not syll.startswith('8') and not syll.startswith('a') and not syll.startswith('E') and not syll.startswith('1') :
                        return ''
                return ''
        
        def add_star(self,word):
                if ('*' in word):
                        return word
                if ('-' in word):
                        return word.replace('-','*', 1)
                
                splitted = word.split('E')
                if len( splitted) > 1:
                         splitted[len(splitted)-2] = splitted[len(splitted)-2]+"*"
                         return 'E'.join(splitted)
                splitted = word.split('U')
                Log('add starx', word)                
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

        
        def simple_o_when_o_ortho(self, syllabe, ortho):
                if 'o' in syllabe  and 'o' in ortho:
                        return syllabe.replace('o','O', ortho.count('o'))
                return syllabe

        def per_as_pr(self, syllabe, ortho):
                return syllabe.replace('peR','pR')


        def long_a_as_ui(self, syllabe, ortho):
                if 'a' in syllabe  and 'â' in ortho:
                        return syllabe.replace('a','8i', ortho.count('â'))
                return syllabe

        def adapt_phonetics(self, phonetics, word):
                result = []
                Log('ortho', phonetics)
                phonetics = self.simple_o_when_o_ortho(phonetics, word)
                phonetics=self.per_as_pr(phonetics,word)
                return self.long_a_as_ui(phonetics, word)
                        

        def concat_ending(self,word,ending):
                if ending.startswith('/'):
                         return word+ending
                endstring= word
                if '/' in word :
                         endstring = word.rsplit('/',1)[1]
                Log('endstring',endstring)

                if [char for char in   ['A', 'E', 'O' , 'U', '*' ,'-'] if  char in endstring]:
                        return word+'/'+ending
                if ending[0]=='R'and 'R' in endstring :
                        return word+'/'+ending
                Log('wtor',endstring)
                return word+ending

        def only_plural(self):
                self.only_plural=true
        
        def newtransform(self,initial_word):
                all_sylls = self.adapt_phonetics(initial_word.phonetics , initial_word.word)
 #                all_sylls = phonetic.replace('-','')

                if initial_word.is_plural() and initial_word.word.endswith('s'):
                       return []

                results = []
                has_homophone = self.has_homophone(initial_word)
                for prefix in self.check_prefixes(initial_word,all_sylls):
                        Log('prefix', vars(prefix))

                        ending =self.check_ending(initial_word,prefix)
                        nextword=prefix
                        if ending:
                                nextword=ending
                                
                        all_suffixes=self.check_suffixes(initial_word,nextword)

                        for suffix in all_suffixes:

                                Log('trouve suffixes', initial_word.word)
                                remains = self.double_consonant_remove_woyel(initial_word.word, suffix.get_remains())
                                Log('trouve suffixes', remains)

                                final_word= Steno_Encoding(remains, prefix.get_steno(), suffix).encode()
                                Log('ending', ending)
                                if ending :
                                        final_word = self.concat_ending(final_word, ending.get_steno())
#                                if has_homophone and initial_word.is_verb() and not prefix.has_ortho_rule() and not ending:
 #                                       Log( 'is homophone',suffix.has_ortho_rule())
  #                                      final_word = self.add_star(final_word)
                                results.append(final_word)
#                        final_word = self.orth_ending_iere(initial_word.word, final_word)

                        if ending and not ending.mandatory:
                                Log('not mandatory')
                                all_suffixes=self.check_suffixes(initial_word,prefix)
                                for suffix in all_suffixes:

                                        Log('trouve suffixes', initial_word.word)
                                        remains = self.double_consonant_remove_woyel(initial_word.word, suffix.get_remains())
                                        Log('trouve suffixes', remains)
                                        final_word= Steno_Encoding(remains, prefix.get_steno(), suffix).encode()
                                        results.append(final_word)
                                
                Log(results)

                for final_word in  results:
                                                
                        Log('final_word' , final_word)
                        results.remove(final_word)
                        
                        Log('final_word' , final_word)
                        results.append(final_word)
                results = list(dict.fromkeys(results))
                return results


        def basic_transform_by_syllabes(self,initial_word):
                all_sylls = initial_word.syll

                if initial_word.is_plural() and initial_word.word.endswith('s'):
                        return []

                results = []
                has_homophone = self.has_homophone(initial_word)
                splitted =all_sylls.split( '-')
                for prefix in self.check_prefixes(initial_word,all_sylls):
                        Log(prefix.get_remains())
                        
                        for suffix in self.check_suffixes(initial_word,prefix):
                                suffix_remains = suffix.get_remains()
                                final_word= Steno_Encoding(suffix_remains, prefix.get_steno(), suffix).encode_by_syll()
                                if has_homophone and initial_word.is_verb() and not prefix.has_ortho_rule() and not suffix.has_ortho_rule():
                                        Log( 'is homophone',suffix.has_ortho_rule())
                                        final_word = self.add_star(final_word)
                                results.append(final_word)
#                        final_word = self.orth_ending_iere(initial_word.word, final_word)


                Log(results)

                for final_word in  results:
                                                
                        Log('final_word' , final_word)
                        results.remove(final_word)
                        
                        Log('final_word' , final_word)
                        results.append(final_word)
                results = list(dict.fromkeys(results))
                return results



