from log import Log
from syllabe import Syllabe
from cutword import Cutword
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
                'Rifi' : '-/FR', # bonus rifi
                'ijO' : 'AO',
#                'jO' : 'RO|AO',
                'jO' : 'AO', # conflit viol et myope RO
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
                'oi' : 'OEU',
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
                'ij' : '-/LZ', #ille
                'aj' : '-/LZ', #paille
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
                '@p' : '-/AFRP' , #campe
                '§p' : '-/OFRP', # trompe
                'pl' : 'PL',
                "ER" : "AIR",
                'gl' : 'TKPWHR|FRLG', #glace or angle
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
                'S' : 'SH|FP',

        }
        VOWELS = {
                "a": "A",       # chat
                "°" : "",
                'j' : 'EU',
                "Z" : "G",
                "H" : "H",
                "5" : "EUPB",
                'u' : 'OU',
                'l' : 'L',

                '1' : 'U',
#                'e' : '',
                "@": "AN",     # pluie
                "E" : "AEU", #collecte
#                "e" : "AEU", #collecte

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
                "8": "U",       # huit
                "§": "ON",
                'N' : 'N',
                'd' : 'D',
                'p' : 'P',
                'm' : 'M',
                'k' : 'K',
                'n' : 'N',

                "y": "U",       # cru

                # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

        }
        needs_star=False
        def __init__(self, syllabes, prefix, suffix):
                if prefix=='TKAOEZ':
                        self.syllabes = self.eat_woyel(self.syllabes)

                self.syllabes = syllabes
                self.prefix = prefix
                self.suffix = suffix
                if '*' in self.suffix and  '/' not in self.suffix:
                        self.suffix = self.suffix.replace('*', '')
                        self.needs_star = True

                Log('steno_suffixes' , vars(self))
        def eat_woyel(self, syll) :
                if not syll[0]:
                        return syll
                Log('> before eat: ', syll[0][:1])
                if syll[0][:1] in ['a','j','u','1','E','e','o','O','8','y' ,'5','2'] :
                        Log('> eat voyel: ', syll)
                        syll[0] = syll[0][1:]
                Log('> not eat voyel: ', syll)
                return syll

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
                                        end = word[len(key):]
                                        if end :
                                                for  findsyll in self.find_matching(syll,end).items():
                                                        syll[findsyll[0]] = findsyll[1]
                                        return syll
                                if word.endswith(key):
                                        start = word[:-len(key)]
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
                Log('-- Encode :',self.syllabes)

                self.word_encoded = ""
                previous = None
                count_syll = 1
                one_hand=False
                next_syll = self.syllabes
                if self.prefix:
                        Log('> Prefix ', self.prefix)
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
                i=0;
                cutword=Cutword(self.syllabes)
                while i<1:
                        i+=1
                        piece=self.syllabes
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
                self.word_encoded = self.word_encoded.replace('//','/')
                if self.needs_star  :
                        splitted = self.word_encoded.split('/')
                        splitted[len(splitted)-1]= self.add_star(splitted[len(splitted)-1])
                        self.word_encoded = '/'.join(splitted)
                if self.word_encoded.endswith('/OU'):
                        self.word_encoded = self.word_encoded.replace('/OU','/O*U')
                return  self.word_encoded
        
        def add_star(self,word):
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
                
                return "*"+word

        def voyels(self, word):
                new_word=word
                for char in word:
                        if char in self.VOWELS:
                                new_word = new_word.replace(char, self.VOWELS[char])
                return new_word
