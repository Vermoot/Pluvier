import sys
import copy
import re
from word import Word
from cutword import Cutword
from syllabe import Syllabe
from log import Log
from steno_encoding import Steno_Encoding
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
#                "s2": "S", # ce mais pas ceux
                "sypER" : "SP-R/",
                "tEkno" : "T",
                "tR@s" : "TRAPBS/",
                "tR@z" : "TRAPBS/",
                "tEl" : "THR-",
                'Egze' : 'KP',
                'Egzi' : 'KPEU',
                'Eksi' : 'KPEU',

                'Eks' : "-/BGS",
                'ade' : 'AD', # sound
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
                "s@t" : "ST",
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
                'a':'A|AE',
                
        }

        ORTHO_PREFIXES = {
                'multi' :OrthoPrefix('mylti', 'PHULT'),
                'corr' : OrthoPrefix('koR', 'KR'),
                'coll' : OrthoPrefix('kol', 'KHR'),
                "comm" : OrthoPrefix('kom|kOm','KPH'),
                "com" : OrthoPrefix('k§','K*/|K'),
                "con" : OrthoPrefix('k§','KOEPB|KOPB'),
                'inter' : OrthoPrefix('5tER', 'EUPBTS'), #SPWR
                'ind' : OrthoPrefix('5d', 'SPW'),
                'end' : OrthoPrefix('@d', 'SPW'),
                'réu' : OrthoPrefix('Rey', 'REU'),
                'fin'  : OrthoPrefix('fin', 'WH'),
                'fen'  :OrthoPrefix('f°n', 'WH'),
                
#                "a" : OrthoPrefix('a-','AE-'), # sound

                }

        
        ORTHO_SUFFIXES = {
                'cation' : OrthoSuffix('kasj§','-BGS'),

                'lation' : OrthoSuffix('lasj§', '-/LGS'),
                'bilité' : OrthoSuffix('bilite','-BLT'),
                'ilité' : OrthoSuffix('ilite','ILT'),
                'lité' : OrthoSuffix('lite','-LT'),
                'bilise' : OrthoSuffix('biliz','BLZ'),
                'ralise' : OrthoSuffix('Raliz','RALZ'),
                'lise' : OrthoSuffix('liz','-LZ'),

                'rité' : OrthoSuffix('Rite', '-RT'), # securite
                'bité' : OrthoSuffix('bite','-BT'),
                'tivité': OrthoSuffix('tivite', '-/TEUFT'),
                'vité': OrthoSuffix('vite', '-/FT'),
                'cité': OrthoSuffix('site', '-/FT'),
                'sité': OrthoSuffix('site', '-ST*E'),
                'igé': OrthoSuffix('iZe', 'EG'),
                'iger': OrthoSuffix('iZe', '-*EG'),
                'ience' : OrthoSuffix('j@s', '-AENS'),
                'ance' : OrthoSuffix('@s', '-NS'),
                'ence' : OrthoSuffix('@s', '-NS'),
                'ande' : OrthoSuffix('@d', '-ND'),
                'aux' : OrthoSuffix('o', '-O*EX'),
                'ité' : OrthoSuffix('ite','ITD'),
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
                'cienne' : OrthoSuffix('sjEn', '-GZ'),
                "telle" : OrthoSuffix("tEl" , "-/LGTS"),
                "tel" : OrthoSuffix("tEl" , "-/LGTS"),
                "velle" : OrthoSuffix("vEl", "-/FL"),
                "quelle" : OrthoSuffix("kEl", "-/BLG"),
                "quel" : OrthoSuffix("kEl", "-/BLG"),
                "elle" : OrthoSuffix("El", "-/*EL"),
                "ière"  : OrthoSuffix('jER', 'A*ER'),
                "ier"  : OrthoSuffix('je', 'AER'),
                'ive' : OrthoSuffix('iv|ive|iv', '-/*EUF'),
                'if' : OrthoSuffix('if', '-/*EUFL'),
                'cien' : OrthoSuffix('sj5', '-GS'),
                "ain" : OrthoSuffix("5", "IN"),
                'cte' : OrthoSuffix('kt', 'KT'),
                "ène" : OrthoSuffix("En","-/*EB"),
#                "eur" : OrthoSuffix("9R","-AO*R"),
                "uel" : OrthoSuffix("yEl","-/U*EL"),
                "uel" : OrthoSuffix("8El","-/W*EL"),
                "anche" : OrthoSuffix("@S","-/AFRPBLG"),
                "rche" : OrthoSuffix("RS","-/FRPB"),
                "che" : OrthoSuffix("S","-/FP"),
                "chage" : OrthoSuffix("SaZ","-/FPG"),
                "oué" : OrthoSuffix("we|wE","-/W*E"),
                "way" : OrthoSuffix("we|wE","-/W*E"),
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
                'mas' : 'MS', #amasse


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
                "@bl": "-/AFRBL",   # tremble
                "§bl": "-/OFRBL",  # comble
                "1bl": "-/UFRBL",  # comble
                "@bR": "-/AFRBS",   # ambre
                "5bR": "-/EUFRBS",  # timbre
                "§bR": "-/OFRBS",   # ombre
                "5b": "-EUFRB",  # limbe
                "§b": "-/OFRB",  # comble
                "ks": "-BGS",
                "t@" : "TAN", #content
                "ve": "-WE", # releve
                "N§" : "-/HO*PB", #bourguignon
                "@Z" :"-/APBLG", # ange
                "5Z" :"-/EUPBLG", # linge
                "§t" : "-/OFRPT", # prompte
                "5p" : "-/EUFRP",
                '@pl' : "-/AFRPL",
                "9R":"-AO*R",
                "je": "AE",     # pied
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
                "@d" :"-/PBD",

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
                "§" : "-/*PB",
#                "sm" : "-/FP",
                'o' : 'OE',
#                't' : 'T',
                'N' : 'PG',
                'El' :'-FL',
                "Z" : "G", # rage
                'u' : 'OU',
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

        def ortho_starting_with_des(self,myword):
                word = myword
                syll = word.syll.replace('-','')
                Log('Starting with des? ', syll)
#                if not syll.startswith('dez') and not syll.startswith('des') and not syll.startswith('d°s'):
                if not word.word.startswith('de') and not word.word.startswith('dé'):
                        return word.syll
                next_letter = word.word[:4].upper()
                Log('> 3rd letter:', next_letter)
                if word.word.startswith('dés') and next_letter[-1] in ['A','E','É','I','O','U', 'Y'] :
                        self.prefix = {'TKAOEZ|STK' : 'dez'}
                        word.syll = word.syll[3:]
                        return word.syll

                if word.word.startswith('dé') or ((next_letter.endswith('O') or next_letter.endswith('E') or next_letter.endswith('I') or next_letter.endswith('A') or next_letter.endswith('U') or next_letter.endswith('@') or next_letter.endswith('Y'))) :
                        
                        if word.syll.startswith('dez'):
                                self.prefix = {'STK':'dez'}
                                word.syll = word.syll.replace('dez', '')
                        if word.syll.startswith('des'):
                                self.prefix = {'STK':'des'}
                                word.syll = word.syll.replace('des', '')
                        if word.syll.startswith('d°s'):
                                self.prefix = {'STK':'d°s'}                                
                                word.syll = word.syll.replace('d°s', '')
                        if (word.syll.startswith('def')):
                                self.prefix = {'STKW' : 'def'}
                                word.syll = word.syll.replace('def', '')
                        if not self.prefix:
                                self.prefix = {'STK' : 'de'}
                                word.syll = word.syll.replace('de', '')
                        Log('> syll: ', word.syll)
                        return word.syll

                return word.syll

        def eat_woyel(self, syll) :
                if not syll[0]:
                        return syll
                Log('> before eat: ', syll[0][:1])
                if syll[0][:1] in ['a','j','u','1','E','e','o','O','8','y' ,'5','2'] :
                        Log('> eat voyel: ', syll)
                        syll[0] = syll[0][1:]
                Log('> not eat voyel: ', syll)
                return syll

                
        def ortho_add_aloneR_infinitif_firstgroup(self, word):
                verb_word = self.find_same_word_verb(word)
                if verb_word.is_verb() and verb_word.is_infinitif()  and verb_word.word.endswith('er'):
                        self.ending = "/-R"
                        self.ending_syll = verb_word.syll
                        if verb_word.syll.endswith('e') :
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word
                return word

        def ortho_add_alone_keys_on_noun(self,word):
                if word.word.endswith('ée'):
                        if not self.ending :
                                self.ending_syll = word.syll[:-1]
                        self.ending = "/-D"

                                
                if word.is_verb():
                        return word
                if word.word.endswith('ette'):
                        self.ending = "/*T"
                        if word.syll.endswith('Et') :
                                Log('Fini par et')
                                self.ending_syll = word.syll[:-2]
                        return word
                return word

        def ortho_suffixes(self,word, syll):
                for orth in self.ORTHO_SUFFIXES.items():
                        if word.endswith(orth[0]) :
                                ortho = orth[1]

                                if ortho.check_alternative :
                                        if not self.find_spelled_word(ortho.get_alternative_str(word,orth[0])):
                                                Log('continue check alternative')
                                                continue
                                Log(vars(ortho))
                                Log('can be' , ortho.can_be_converted(syll))
                                if (ortho.can_be_converted(syll)):
                                        syll = ortho.convert(word, syll)
                                        Log('converted ok',syll)
                                                                                
                                        self.suffix = ortho.steno()
                                        return syll
                return syll

        def ortho_prefixes(self,word, syll):
                Log('ortho_prefixes start')
                for orth in self.ORTHO_PREFIXES.items():
                        if word.startswith(orth[0]):
                                Log(vars(orth[1]))
                                ortho = orth[1]
                                ortho.prefix = True

                                if (ortho.can_be_converted(syll)):
                                        syll = ortho.convert(word,syll)
                                        self.prefix = {ortho.steno() : ortho.sound}
                                        Log('prefix test' , self.prefix)
                                        return syll
                return syll

        
        def ortho_add_alone_keys_on_verb(self,word, phonetics):
                verb_word = self.find_same_word_verb(word)

                if not verb_word.is_verb():
                        return word
                if verb_word.has_noinfoverb():
                        return word

                Log('Verbe')
                
                if (not self.ending_syll):
                        self.ending_syll = phonetics
                        
                if  verb_word.is_passe_compose():
                        if verb_word.word.endswith('ué') or verb_word.word.endswith('oué') :
                                self.ending = "/W*E"
                                self.ending_syll = verb_word.syll[:-2]
                                return verb_word
                        if verb_word.syll.endswith('e') :
                                self.ending = "/-D"
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word
                if verb_word.is_conditionnel():
                        self.ending = "/-RS"
                        if verb_word.is_third_person_plural():
#                                self.ending = "AEUPBT"
                                self.ending = "/-RPB"
                                self.ending_syll = verb_word.syll[:-1]
                                return verb_word
                        if verb_word.word.endswith('rais') and verb_word.syll.endswith('E') :
                                self.ending = "/-RS"
                                if verb_word.word.endswith('rait'):
                                        self.ending = "-RTS"

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

                if verb_word.ending_with('ais'):
#                if verb_word.is_imparfait():
                        Log('imparfait')
                        self.ending = "/-S"
#                        self.ending = "/AEUS"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word
                if verb_word.ending_with('ait'):
#                        if verb_word.is_third_person_singular():
#                                self.ending = "/AEUT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        self.ending = "/AEUT"
                        return verb_word

                if verb_word.ending_with('aient'):
#                        if verb_word.is_third_person_plural():
#                                self.ending = "AEUPBT"
                        self.ending = "AEUPBT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        return verb_word
                if verb_word.ending_with('ait'):
#                        if verb_word.is_third_person_singular():
#                                self.ending = "/AEUT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        self.ending = "/-TS"
                        return verb_word

                if verb_word.ending_with('ent'):
#                        if verb_word.is_third_person_singular():
#                                self.ending = "/AEUT"
                        if verb_word.syll.endswith('E') :
                                self.ending_syll = verb_word.syll[:-1]
                        self.ending = "/-T"
                        return verb_word

                # if verb_word.syll.endswith('E') :
                #         self.ending_syll = verb_word.syll[:-1]

                if not self.ending  :
                        Log('not found ending',verb_word)
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
                cutword = Cutword(word_class.word)
                if (word_class.word.startswith('y') and word.startswith('j')):
                        self.prefix ={'KWR' : 'j'}
                        new_word = word.replace('j','',1)
                        cutword.set_remains(word.replace('j','',1))
                        cutword.set_replaced_by('j','KWR')
                        return new_word
                
                new_word=word
                if  self.pronoun:
                        self.prefix={'Y': 'y'}
                        return word
                for prefix in  self.PREFIXES.items():
                        if len(re.split("^"+prefix[0], new_word))>1:
                                
                                Log('found prefix : ',prefix[0])
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
                Log('The word is a verb ? ' , myword.is_verb())
                has_homophone = self.has_homophone(myword)
                Log('Has homophone ? ' , has_homophone)
                finals = self.final_encoded
                Log('Final words encoded: ' , self.final_encoded)
                return self.final_encoded

        def prefix_h(self, word, syll) :
              
                if word.startswith('h') :
                        self.prefix = {'H' : ''}
                #and not syll.startswith('8') and not syll.startswith('a') and not syll.startswith('E') and not syll.startswith('1') :
                        return ''
                return ''
        
        def get_prefix_and_suffix(self, initial_word, check_prefix = True, check_suffix = True ) :
                word = initial_word
                self.prefix ={}
                self.prefix_h(initial_word.word, initial_word.syll)
                self.suffix =""
#                word_str = self.change_syllabes(word.syll)
                phonetics  = word.syll.replace('-','') #word_str.split('-')
                if check_prefix:
#                        self.orth_write_ending_d(word)
                        phonetics = self.ortho_prefixes(word.word, phonetics)
                if check_suffix:
                        phonetics = self.ortho_suffixes(word.word, phonetics)
                        Log('get suffix', self.suffix)
                        if not self.suffix:
                                word = self.ortho_add_aloneR_infinitif_firstgroup(word)
                                word = self.ortho_add_alone_keys_on_verb(word,phonetics)
                                word = self.ortho_add_alone_keys_on_noun(word)
                word.syll = phonetics
                if check_prefix and not self.prefix:
                        phonetics = self.ortho_starting_with_des(word)
                Log('suffix', self.suffix)

#                word_str  = word_str.replace('-','') #word_str.split('-')
                self.prefix_h(word.word, word.syll)

                Log('self prefix', self.prefix)                        
                Log('before prefix', phonetics)
                if check_prefix and not self.prefix:
                        phonetics = self.prefixes(phonetics, word)
                Log('after prefix', phonetics)
                Log('suffix', self.suffix)

                if check_suffix and (not self.suffix and '-' in word.syll and not self.ending):
                        phonetics = self.real_suffixes(phonetics)
                if check_suffix and not self.suffix and not self.ending:
                        phonetics = self.suffixes(phonetics)
                Log('suffix', self.suffix)

                return phonetics

        def transform_word(self,initial_word):
                myinitial_word= copy.copy(initial_word)
                all_sylls = initial_word.syll.replace('-','')
                all_sylls = self.double_consonant_remove_woyel(initial_word.word, all_sylls)


                if myinitial_word.is_plural() and myinitial_word.word.endswith('s'):
                        return []

                word_str = self.get_prefix_and_suffix(myinitial_word)
                
                self.syllabes = [word_str]
                Log('syllabe',self.syllabes)
                Log('ending',self.ending)
                Log('ending_syll',self.ending_syll)

                for aprefix, phonem  in self.prefix.items():
                        for  one_prefix in aprefix.split('|'):
                                self.syllabes = [word_str]                                        
                                if one_prefix=='TKAOEZ':
                                        self.syllabes = self.eat_woyel(self.syllabes)

                                if not self.ending: 
                                        self.final_encoded.append(Steno_Encoding(self.syllabes, one_prefix, self.suffix.split('|')[0]).encode())

                                if self.ending :
                                        self.final_encoded.append(Steno_Encoding(self.syllabes, one_prefix, self.suffix.split('|')[0]).encode()+self.ending)

                                        # myendingword =  initial_word
                                        # myendingword.syll= self.ending_syll
                                        # word_str = self.get_prefix_and_suffix(myendingword,True,True)
                                        # Log('endi : ',word_str)
                                        # suff = ""
                                        # Log('suffix endi', suff)
                                        # if one_prefix=='TKAOEZ':
                                        #         self.syllabes = self.eat_woyel(self.syllabes)
                                        
#                                self.syllabes = [word_str]
#                                self.prefixes(self.ending_syll, word)
#                                suff =self.suffix.split('|')[0]


                                     #   self.final_encoded.append(Steno_Encoding(re.sub( "^"+ phonem, '', self.ending_syll).split('-'), one_prefix, suff).encode()+self.ending)

#                word_str = self.get_prefix_and_suffix(initial_word)
#                self.syllabes = [word_str]

                for  one_suffix in self.suffix.split('|'):
                        prefix = ""
                        if self.prefix: 
                                prefix = list(self.prefix.keys())[0].split('|')[0]
                        if not self.ending :
                                self.final_encoded.append(Steno_Encoding(self.syllabes,  prefix, one_suffix).encode())
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
                        encoded_w = Steno_Encoding([self.ending_syll.replace('-', '')], "",self.suffix).encode()+self.ending
                        Log('ending encoding: ', encoded_w)
                        self.final_encoded.append(encoded_w)



                
                Log('> syl',initial_word.syll)
                if ('H' in self.prefix):
                        all_sylls = 'H'+all_sylls
                all_sylls =[all_sylls]
                Log('> all syl',all_sylls)
                if not self.ending and not initial_word.is_verb() :
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
                self.final_encoded = list(dict.fromkeys(self.final_encoded))
                return  self.final_encoded
        


