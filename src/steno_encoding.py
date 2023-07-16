from src.log import Log
from src.syllabe import Syllabe
from src.cutword import Cutword
class Steno_Encoding:
        
        CHUNKS = {
                # syllabe of sound
                # separate by |  => right_hand|left_hand
                # start with / : already encoded
                # start with - : right hand
                'sjasj§': '/SRAGS', #ciation
                '@v°n' : 'ENVH',
                'sal': 'sl',
                "aOR" : "/ARP",
                "pRasj§":"/RPGS",
                'ynik' : 'UBG',
                "enER": "EBS",
                '§ple' : '/OFRPL', # trompe
                '5ba' : '/EUFRB', # trimb            
                '§pli' : '/OFRPL', # trompe

                'v°n' : 'WH|FPB',
                'vin' : 'VH',

                'vOl' :'VL',
                'ekil' :'KL',
                "jEn": "AEB",
                'Egze' : '/KP',
                'Egzi' : '/KPEU',
                'Eksi' : '/KPEU',
                'Eks' : '/KP',
                'ek' : 'K',

                
#                'ist' : '*EUS',
                'm°n' : "/KH",#men
                'min' : "/KH",#min
                'm2n' : '/KH', #men
                'mn' : '/KH', #menb
                
                'wan' : 'WOIB', #douane                
                'bRe': '-/BS',
                "djO": "OD",
                "zj§": "-/GZ",

                'nal' : '-/PBL', 
                '@kR' : '/AFRBGS', #cancre
                "sj§": "-/GZ",
                'vul': '/WHR',
                "fik" : "-/FBG",
                "fEk" : "-/FBG",
                                'kE' : 'KE',
                'psjOn' :'-/PGS',
                'ps' : 'S',
                'sjOn' :'-/GZ',
                'vERn' : '-/FRB', # gouverne
                'vERs' : '-/FRB', # divers
                'ERv' : '-/FRB', #v-erve

                
                'vEr' : '-/FRB', # cou-vert
                'vER' : '-/FRB', # travers
                'Rifi' : '-/FR', # bonus rifi
                'ijO' : 'AO',
#                'jO' : 'RO|AO',
#                'jO' : 'AO', # conflit viol et myope RO
                'j@' : 'AEN' , # son ian
                '@l' : 'ANL', #enleve
                "RSi" : "VRPB",
                'REj' : '-/RLZ' , #oreille

                "tER": "TAEUR|TS",  #notaire
                "EtR" : "-/TS" , #fenetre
                "RS" : "VRPB",# -rche
                "dZEk" : "-/PBLG",
                "dZ" : "-/PBLG",
                "bZEk" : "-/PBLG",
                "bZ" : "-/PBLG",
                "ps" : "S",
                "pR":"PR|PS", #-pre
                'stR' : 'STR|-/TS',#new rule
                'st' : 'ST|FT',#new rule
                'En' : 'AIB',
                'eO' : 'AOU',
                'eo' : 'AOU',
                'oi' : 'OEU',
                'v@' : "WAPB|FG",
                "vaj" : "-/FL",
                "vEj" : "-/FL",
                #'@v' : 'ENVH', #envenime
#                'vwa' : 'WOEU',# not in TAO rules..
                't8' : 'TW', # fru-ctu-eux
#                "kR" : "KR", 
                "ks": "-/BGS",
                '8a' : 'WA' , # ua in situation
#                "kR" : "RK",#can-cre
                 "kR" : "KR|RBG",#skrute
                'Ne'  : '-/PG',
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
                'el': 'L',
                "je": "AE",     # pied
                "jE": "AE",     # ciel
                "ja": "RA",     # cria
                "rjO": "RAO",     # griotte
                "jO": "AO",     # kiosque

#                "jO": "ROE",    # fjord # TODO unsure
#                "jo": "AO",     # bio # TODO Some conflict there. "-R can be read as i" (above), but the diphtongs are more important I guess?
#                "jO": "RO",     # fjord
                "j§": "AO",     # av_ion_
                "kw": "KW",
                'k§' : 'KOPB', # content
#                "wE": "WAEU",
                "wE" : "WE",
                "fR" : "/TPR|/FR",
                "§t" : "OFRPT",
                "@S" : "/AFRPBLG",
                "5S" : "/EUFRPBLG",
                '@p' : '/AFRP' , #campe
                '§p' : '/OFRP', # trompe
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
#                "ij": "/LZ",    # bille # TODO Maybe not a diphtong, but a word ending/consonant thing

                'fl': "FL",
                "ska" : "K",#skrute
                "sk" : "K",#skrute
                "sp" : "SP|P",#espoir
                'S' : 'SH|FP',
                "5" : "/EUPB",
                'n' : 'TPH|B',
                'N' : '-PG|PG',
                "@": "/APB",     # pluie
        }
        ALONE_SUFFIXES = {
                'OU' : 'O*U',
                '-PB': '-*PB',
                'OEUB' : 'O*EUB'
        }
        VOWELS = {
                "a": "A",       # chat
                "°" : "",
                'j' : 'EU',
                "Z" : "J",
                "H" : "H",

                'u' : 'OU',
                'l' : 'L',

                '1' : 'U',
#                'e' : '',

                "e": "E",       # clé
                "E" : "AEU", #collecte
#                "e" : "AEU", #collecte

                "2": "AO",      # eux
                "9": "AO",      # seul
#                "E": "AEU",     # père


#                "E" : "",
                "i": "EU",      # lit
                "o": "OE",      # haut
                "O": "O",       # mort

#                "y" : "",
                "u": "OU",      # mou
                "8": "U",       # huit
                "§": "ON",
                'd' : 'D',

                'p' : 'P',
                'm' : 'M',
                'k' : 'K',
                'n' : 'N',
                's' : 'S',

                "y": "U",       # cru

                # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

        }
        needs_star=False
        def __init__(self, syllabes, prefix, suffix):
                self.syllabes = syllabes
                if prefix=='TKAOEZ':
                        self.syllabes = self.eat_woyel(self.syllabes)


                self.prefix = prefix
                self.suffix = suffix
                if '*' in self.suffix.get_steno() and  '/' not in self.suffix.get_steno():
                        self.suffix.remove_star()
                        Log('nedd star')
                        self.needs_star = True

                Log('steno_suffixes' , vars(self.suffix))
        def eat_woyel(self, syll) :
                if not syll or not syll[0]:
                        return syll
                Log('> before eat: ', syll[0][:1])
                if syll[0][:1] in ['a','j','u','1','E','e','o','O','8','y' ,'5','2'] :
                        Log('> eat voyel: ', syll)
                        syll = syll.replace(syll[0][1:],'',1)
                Log('> not eat voyel: ', syll)
                return syll

        def diphtongs_try(self, word):
                new_word=word
                final_word = ''
                items = self.CHUNKS
                keys = self.CHUNKS.keys()
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
                list_tuple=[]
                for sound, steno in self.CHUNKS.items():
                        if not sound in word:
                                continue
                        Log('Find sound:', sound)
                         #                                self.found_sound = diphtong[1]
                        if word.startswith(sound):
                                list_tuple.append((sound,steno)) 
                                end = word[len(sound):]
                                if end :
                                        for  newkey, value in self.find_matching(syll,end):
                                                list_tuple.append((newkey,value)) 
                                return list_tuple
                        if word.endswith(sound):
                                start = word[:-len(sound)]
                                if start :
                                        for  key, value in self.find_matching(syll,start):
                                                list_tuple.append((key,value)) 
                                list_tuple.append((key,steno))
                                return list_tuple

                        splitted = word.split(sound)
                        start  =splitted[0]
                        for  newkey,value in self.find_matching(syll,start):
                                list_tuple.append((newkey,value)) 
                        list_tuple.append((sound,steno))     
                        end = splitted[1]
                        for  newkey,value in self.find_matching(syll,end):
                                list_tuple.append((newkey,value)) 
                        return list_tuple
                list_tuple.append((word, ""))

                return list_tuple
                                
                                
        def diphtongs(self, word):
                before = ''
                after = ''
                new_word=word
                syll_dict = {}
                final_word = word
                items = self.CHUNKS
                keys = self.CHUNKS.keys()
#                self.found_sound = ''
                nb_char = len(word)
                for diphtong in self.CHUNKS.items():
                        
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


                        self.word_encoded = previous.encoded()
                        if (one_hand):
                                previous.change_hand_to_left(True)
                                self.word_encoded=self.word_encoded+'/'

                        Log('prefix encoded', self.word_encoded)
                        count_syll = 2
                i=0;
                cutword=Cutword(self.syllabes)
                while i<1:
                        i+=1
                        piece=self.syllabes
                        if piece == "":
                                continue
                        Log('one piece',piece)
                        sylls = {}
                        sylls = self.find_matching(sylls, piece)
                        Log('find matching sylls: ' , sylls)

                        
                        if piece == "":
                                continue

                        for key,new_piece in sylls :
                                Log(f'key:{key}, new_piece:{new_piece}')
                                if new_piece == "":
                                        new_piece = self.voyels(key)
                                        new_piece = new_piece.upper()
                                one_hand = False
                                syllabe = Syllabe(new_piece.upper(), previous,next_syll)
                                encoded = syllabe.encoded()
                                Log('Encoded syllabe',encoded)
                                if previous:
                                        Log('previous',vars(previous))
                                Log('encoded syllabe', encoded)
                                self.word_encoded = self.word_encoded+encoded
                                Log('encoded word', self.word_encoded)
                                previous = syllabe
                        next_syll = self.syllabes[count_syll:]
                        count_syll = count_syll+1
                Log('WORD ENCODED BEFORE SUFFIX', self.word_encoded)
                if self.suffix and self.suffix.has_separate_stroke() :
                        self.word_encoded = self.word_encoded + self.suffix.get_steno()
                        Log('word enc:', self.word_encoded)
                if self.suffix and not self.suffix.has_separate_stroke() :
                        syllabe = Syllabe(self.suffix.get_steno(),previous, next_syll).suffix()
                        Log('word enc 2:', self.suffix)
                        self.word_encoded = self.word_encoded + syllabe.encoded()

                if self.word_encoded.startswith('/'):
                        self.word_encoded = self.word_encoded[1:]
                if self.word_encoded.endswith('/'):
                        self.word_encoded = self.word_encoded[:-1]
                Log('WORD ENCODED ', self.word_encoded)
                self.word_encoded = self.word_encoded.replace('//','/')
                if self.needs_star  :
                        splitted = self.word_encoded.split('/')
                        splitted[len(splitted)-1]= self.add_star(splitted[len(splitted)-1])
                        self.word_encoded = '/'.join(splitted)
                for alone, replaced_by in self.ALONE_SUFFIXES.items():
                        if self.word_encoded.endswith('/'+alone):
                                self.word_encoded = self.word_encoded.replace('/'+alone,'/'+replaced_by)
                
                return  self.word_encoded
        

        def encode_by_syll(self):
                Log('-- Encode by syllabes :',self.syllabes)

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

                        count_syll = 2
                        previous.keys_left= ''
                i=0;
                cutword=Cutword(self.syllabes)
                for piece in self.syllabes.split( '-'):
                        if piece == "":
                                continue
                        Log('piece',piece)
                        sylls = {}
                        sylls = self.find_matching(sylls, piece)
                        Log('sylls' , sylls)
                        Log('word encoded' , self.word_encoded)
                        
                        if piece == "":
                                continue
                        
                        for mysyll in sylls.items() :
                                new_piece = mysyll[0]
                                Log('syllabe:',new_piece)
                                if mysyll[1] != "":
                                        new_piece = mysyll[1]
                                else:
                                        new_piece = self.voyels(new_piece)
                                        new_piece = new_piece.upper()

                                Log('syllabe ici :',new_piece)
                                syllabe = Syllabe(new_piece.upper(), previous,next_syll)
                                encoded = syllabe.encoded()

                                Log('encoded syllabe', encoded)
                                
                                self.word_encoded = self.word_encoded+ encoded
                                
                                Log('encoded word', self.word_encoded)

                                previous = syllabe
                        previous.keys_left= ''
                        next_syll = self.syllabes[count_syll:]
                        count_syll = count_syll+1

                Log('WORD ENCODED BEFORE SUFFIX', self.word_encoded)
                if self.suffix :
                        if self.suffix.has_separate_stroke():
                            self.word_encoded = self.word_encoded + suffix.get_steno()
                        else :
                                syllabe = Syllabe(self.suffix.get_steno(),previous, next_syll).suffix()
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
        def voyels(self, word):
                new_word=''
                for char in word:

                        Log('replace',char)
                        transform_char=char.upper()
                        if char in self.VOWELS:
                                transform_char=self.VOWELS[char]
                        Log('by',transform_char)
                        new_word = new_word+transform_char
                return new_word
