import sys
import copy
import re
class Cutword:
        remains = ''
        steno  = ''
        ortho_rule=False
        separate_stroke=False
        def __init__(self,phoneme):
            self.phoneme = phoneme
            self.remains = phoneme
            self.found=False
        def __str__(self):
                return self.phoneme

        def has_found(self) :
                return self.found

        def has_ortho_rule(self) :
                return self.ortho_rule

        def has_separate_stroke(self) :
                return self.separate_stroke

        def set_ortho_rule(self) :
                self.ortho_rule=True
                return self

        def remove_star(self) :
                self.steno=self.steno.replace('*', '')
                return self

        def set_separate_stroke(self) :
                self.separate_stroke=True
                return self

        def generate(self) :
                mylist = []
                if not self.steno:
                        mylist.append(self)
                        return mylist
                splitted = self.steno.split('|')

                for sound in splitted:
                        newcut=Cutword(self.phoneme)
                        newcut.set_remains(self.remains)
                        newcut.set_replaced_by(self.replace, sound)

                        if self.has_ortho_rule():
                                newcut.set_ortho_rule()
                        if self.has_separate_stroke():
                                newcut.set_separate_stroke()

                        mylist.append(newcut)
                return mylist
        def get_remains(self):
                return self.remains
        def set_remains(self, remains):
                self.remains=remains
                return self
        def set_replaced_by(self, replace,by):
                self.replace=replace
                self.steno=by
                self.found=True
                return self
        
        def get_steno(self) :
                return self.steno
