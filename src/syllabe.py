from src.log import Log
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
                if self.previous is not None and previous_encoded.endswith('-'):
                        Log('add hyphen previous encod',previous_encoded)
                        return word

                if not (self.hand == 'R' and (self.previous.hand == 'L')):
                        return word

                if  self.contains_woyels( previous_encoded) or self.contains_woyels(word):
                        return word

                Log('added hyphen to word',word)

                return "-"+word
        def encode_syll(self, syllabe, sounds,keys,already_encoded):
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
                                encoded_hand=encoded_hand + key_trans
                return [encoded_hand,keys,rest,not_found]

        
        def add_hyphen_between(self, encoded_hand, word,already_encoded, previous ):

                if already_encoded :
                        return word
                Log('hand', self.hand)
                Log('word', word)

                if previous is None and self.hand == 'R'  and self.already_encoded == "" :
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

                Log('added hyphen to word',word)

                return "-"+word
                

        def consume(self,syllabe, keys, sounds):
                keys = keys
                not_found = []
                rest = ''
                if not self.encoded_hand:
                        self.encoded_hand = ''
                Log('--- Consume ---')
                Log('syll:',syllabe)
                Log('hand:',self.hand)
                Log('previous:',self.previous)
                Log('encoded hand:',self.encoded_hand)
                Log('already_encoded ? ',self.already_encoded)
                if not self.already_encoded:
                        self.already_encoded= ''
#                if self.already_encoded :
 #                       keys = keys.split(syllabe[-1:])[1] if len(keys.split(syllabe[-1:]))>1 else ''n
 #                       Log('alreday keys left',keys)

                        
                if ("|" in syllabe) :
                        syllabe_split = syllabe.split('|')[0]
                        self.already_encoded = True
                        if self.is_right_hand() and len(syllabe.split('|'))>1:
                                syllabe_split = syllabe.split('|')[1]
                        if not self.syll_can_enter(syllabe_split, keys):
                                if self.is_right_hand():
                                        self.encoded_hand=self.encoded_hand+'/'
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
                [encoded, keys ,rest,not_found] =self.encode_syll(syllabe,sounds,keys,self.already_encoded)
                Log('hand:',self.hand)
                Log('contains voyelles:',self.contains_woyels(syllabe))
                if (self.is_right_hand() and not self.contains_woyels(encoded)  and not self.contains_woyels(self.encoded_hand) and  self.previous) and not syllabe.startswith( '-'):
                        Log('previous:',self.previous.encoded_hand)
                        if self.previous.hand=='L' and not self.contains_woyels(self.previous.encoded_hand):
                                self.encoded_hand =self.add_hyphen_after(self.encoded_hand)

                if (self.is_right_hand() and not self.contains_woyels(encoded) and not self.contains_woyels(self.encoded_hand) and  not self.previous and not syllabe.startswith( '-')):
                        self.encoded_hand =self.add_hyphen_after(self.encoded_hand)
                Log('keys left',keys)

                Log('encoded',encoded)
                Log('keys left',keys)
                self.encoded_hand = self.encoded_hand+encoded
                Log('not_found', not_found)
                Log('encoded', self.encoded_hand)
                Log('rest', rest)
                Log('keys left', keys)
                self.keys_left = keys
                return (rest,not_found)

        def add_hyphen_after(self,syllabe):
                if '-' not in syllabe:
                        return syllabe + '-'
                return syllabe
         
                
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
                Log('--- Encoded ---')
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
                

                add_underscore=False
                if self.syllabe.startswith('-') :
                        self.syllabe = self.syllabe[1:]
                        add_underscore=True
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
                        
                Log('encoded_hand bf', self.encoded_hand)
                while rest and count<30:

                        if  self.is_left_hand() and cpt:
                                cpt = False
                                self.encoded_hand = self.encoded_hand+'/'
                                if add_underscore:
                                        self.encoded_hand=self.encoded_hand +'-'
                                                                        

#                                piece = piece+'/'
                        (rest, not_found) = self.consume_syll(rest)

                        Log('piece',self.encoded_hand)

                        if rest :
                                self.change_hand()
                                cpt = True
                        count= count +1
                        Log('reste:'+rest)
                        Log('encoded_hand', self.encoded_hand)
#                self.encoded_hand = self.add_hyphen(self.encoded_hand)
                Log('-- Encoded : end --')
                return self.encoded_hand #piece

        def replace_hand(self, syllabe, items):
                for sound in items:
                        syllabe = syllabe.replace(sound[0], sound[1])
                return syllabe

