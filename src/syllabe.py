from src.log import Log
from copy import copy
class Syllabe:
        hand = 'L'

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
                "n" : "B",
#                "A" : "Z",
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
                "n" : "TPH",
                "Q" : "KW",
                'X' : 'KP',
                "N": "TPH",
                "Z" : "SWR"

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
                        Log('get previous key left:',previous.keys_left)
                        self.keys_left = previous.keys_left

                if syllabe =="":
                        Log('init key left because syllabe is empty:')
#                        self.init_keys_left()
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

        def change_hand_to_left(self, force=False):
                if self.is_left_hand() and not force:
                        return self;
                self.hand='L'
                Log('change_hand to Gauche')
                self.init_keys_left()
                if not self.encoded_hand.endswith('/'):
                        self.encoded_hand= self.encoded_hand+'/'
                return self

        def change_hand_to_right(self):
                if self.is_right_hand():
                        return self;
                self.hand='R'
                Log('change_hand to Droite')
                self.init_keys_left()

                Log('keys left',self.keys_left)
                return self
        
        def change_hand(self):

                if self.is_right_hand():
                        return self.change_hand_to_left()
                self.hand='R'
                Log('change_hand to Droite')
                self.init_keys_left()
                return self
        
        def is_right_hand(self):
                return self.hand == 'R'

        def is_left_hand(self):
                return self.hand == 'L'

        def contains_woyels(self, syll) :
                word = syll.split('/')[-1]
                return "*" in word or "A" in word or "O" in word or "E" in word or "U" in word
                
        def add_hyphen(self, word):
                Log(f'add hyphen : hand {self.hand}, word {word}')
                if self.already_encoded :
                        return word

                if self.previous is None and self.hand == 'R'  and self.already_encoded == "" :
                        return '-'+word
                
                if self.previous is None :
                        return word
                previous_encoded = self.previous.encoded_hand
                if (self.encoded_hand != '') :
                        previous_encoded = previous_encoded + self.encoded_hand
                if self.previous is not None and previous_encoded.endswith('-'):
                        Log('add hyphen previous encod',previous_encoded)
                        return word

                if not (self.hand == 'R' and (self.previous.hand == 'L')):
                        return word

                if  self.contains_woyels( previous_encoded) or self.contains_woyels(word):
                        return word

                Log('added hyphen to word:',word)
                return "-"+word

        
        def encode_syll(self, syllabe, sounds,keys,already_encoded):
                Log(f'encode_syll syllabe: {syllabe}, sounds:{sounds}, keys:{keys}')
                not_found = []
                rest = ''
                encoded_hand= ''
                for key in syllabe:
                        if not_found:
                                rest=rest+key
                                Log('not found',rest)
                                continue
                        key_trans = key
                        if not already_encoded and ( key in sounds.keys()):
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
                                Log('encoded hand ',encoded_hand)
                                
                        if not not_found:
#                                self.encoded_hand = self.encoded_hand + self.add_hyphen(key_trans)
                                encoded_hand=encoded_hand+key_trans
                return [encoded_hand,keys,rest,not_found]

        
        def add_hyphen_between(self, first, end):
                Log(f'add hyphen between :{first}, end:{end}, hand:{self.hand}')
                if (self.contains_woyels(end)): 
                        return  first + end                
                if (self.is_right_hand() and first  =='/' and end) :
                        return  first + '-'+end;
        
                if (self.is_left_hand()):
                        return first+end

                if not end :
                        return first
                if not first:
                        if ((not self.previous
                            or (self.previous.hand=='L'
                                and not self.contains_woyels(self.previous.encoded_hand)))):
                                return '-'+end
                        return end
                if (self.previous and self.previous.hand=='R') :
                        return  first + end
                start = first.split('/')[-1]

                if not start and self.contains_woyels(end):
                        return first+end
                if not start :
                        return first+'-'+end

                if self.contains_woyels(start):
                        return first+end
                
                if self.contains_woyels(end):
                        return first+end

                if first.endswith('-') or end.startswith( '-'):
                        return first + end
                return first+"-"+end
                
        def log_instance(self):
                if self.previous:
                        Log('previous:', vars(self.previous))
                Log('hand:',self.hand)
                Log('encoded hand:',self.encoded_hand)
                Log('already_encoded ? ',self.already_encoded)
                
        def consume(self,syllabe, keys, sounds):
                not_found = []
                rest = ''
                if not self.encoded_hand:
                        self.encoded_hand = ''
                Log( f'--- Consume {syllabe}---')
                Log('sounds:',sounds)
                Log('keys:',keys)
                self.log_instance()
                if not self.already_encoded:
                        self.already_encoded= ''
                        
                if ("|" in syllabe) :
                        syllabe_split = syllabe.split('|')[0]
                        self.already_encoded = True
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
                        Log('syll split:',syllabe_split)
                [encoded, keys ,rest,not_found] = self.encode_syll(syllabe,sounds,keys,self.already_encoded)
                Log(f'encoded: {encoded}, keys:{keys}, rest:{rest}, not_found:{not_found}')
                Log('hand:',self.hand)
                self.encoded_hand = self.add_hyphen_between(self.encoded_hand,encoded)
                Log('after encoded_hand',self.encoded_hand)
                Log('keys left', keys)
                self.keys_left = keys
                Log(f'return rest: {rest},not_found:{not_found}')
                return (rest,not_found)
        
        def is_first_stroke(self):
                return not self.previous
                
                
        def add_hyphen_after(self,encoded):
                Log('add hyphen after self', self.encoded)
                Log('add hyphen after', encoded)
                if (self.is_left_hand()
                    or self.contains_woyels(encoded)):
                        return self.encoded_hand


                if ( self.previous
                    and not encoded.startswith( '-')):
                        Log(f'here previous:hand {self.previous.hand}, encoded_hand:{self.previous.encoded_hand}')
                        if self.previous.hand=='L' and not self.contains_woyels(self.previous.syllabeg):
                                return self.encoded_hand + '-'

                if ( not self.previous
                    and not encoded.startswith( '-')):
                        return self.encoded_hand + '-'


                return self.encoded_hand
                         
        def consume_syll(self, syllabe):
                sounds = self.SOUNDS_LH
                if self.is_right_hand():
                        sounds = self.SOUNDS_RH
                Log('consume syll keys_left',self.keys_left)
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
                Log('> Function: syll_can_enter:'+syll)
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
                                encoded = encoded + key_trans

                return (encoded,rest,not_found)

        def needs_hand(self, syllabe, already_encoded) :
                (encoded,rest,not_found) = self.get_hand_sound('L',syllabe,already_encoded)
                if not encoded :
                        Log('needs right hand',rest)
                        return 'R'
                (encoded,rest,not_found) = self.get_hand_sound('R',syllabe,already_encoded)
                if not rest:
                        Log('need left hand')
                        return 'L'
                Log('need both hand')
                return 'B'

                        
        def matching_syll(self, syllabe, keys) :
                for car in syllabe:
                        if car not in keys:
                                return False
                        keys = keys.replace(car,'')
                return True

        def encoded(self):
                piece = ""
                Log('--- Encoded ---')
#                self.encoded_hand = ''

                if self.syllabe == "":
                        return piece


                        
                if self.is_prefix:
                        # prefix always start left hand
                        self.hand = 'L'
                        self.already_encoded = True
                        self.init_keys_left()

                        Log('encoded one_hand', self.syllabe)

                        if self.syllabe.endswith('-'):

                                self.syllabe = self.syllabe[:-1]                    
                

                add_hyphen=False
                if (self.previous is not None) :
                        if "PBLG" in self.previous.encoded_hand:
                                self.change_hand()
                                cpt = True
                        else:
                                self.keys_left = self.previous.keys_left
                if self.syllabe.startswith('-') :
                        self.syllabe = self.syllabe[1:]
                        add_hyphen=True
                        Log('has hyphen so change to right')

                if self.syllabe.startswith('/'):
                        self.already_encoded = True
                        self.syllabe = self.syllabe[1:]          

                rest = self.syllabe
                count = 1

                cpt = (self.has_previous_R_and_L())
                                                                
                if self.is_suffix :
                        Log('is suffix')
                        need_hand = self.needs_hand(self.syllabe, self.already_encoded)

                        if need_hand == 'B' :
                                Log('need hand' , need_hand)
                                self.change_hand_to_left()
                                cpt= True
                        
                Log('encoded_hand bf', self.encoded_hand)
                while rest and count<30:
                        if add_hyphen:
                                self.change_hand_to_right()
                        if  self.is_left_hand() and cpt:
                                cpt = False

                        (rest, not_found) = self.consume_syll(rest)

                        Log('piece',self.encoded_hand)

                        if rest :
                                if rest!=self.syllabe :
                                        self.previous=copy(self)
                                self.change_hand()
                                cpt = True
                        count= count +1
                        Log('reste:'+rest)
                        Log('encoded_hand', self.encoded_hand)



                Log('-- Encoded : end --')

                return self.encoded_hand #piece

        def replace_hand(self, syllabe, items):
                for sound in items:
                        syllabe = syllabe.replace(sound[0], sound[1])
                return syllabe

